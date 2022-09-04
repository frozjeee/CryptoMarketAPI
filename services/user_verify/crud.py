from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from schemas import UserVerify, UserId
import configs.kafkaConfig as kafkaConfig
import configs.config as config
import idanalyzer


async def verifyUser(
        settings: config.Settings = config.getSettings(),
        kafkaSettings: kafkaConfig.Settings = kafkaConfig.getSettings()):
    consumer = AIOKafkaConsumer(
                kafkaSettings.USER_VERIFY_TOPIC,
                loop=kafkaSettings.loop(),
                bootstrap_servers=kafkaSettings.KAFKA_BOOTSTRAP_SERVERS,
                group_id=kafkaSettings.USER_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            try:
                payload = UserVerify.parse_raw(msg.value)

                coreapi = idanalyzer.CoreAPI(
                            settings.ID_ANALYZER_API_KEY, 
                            settings.ID_ANALYZER_REGION)
                            
                coreapi.throw_api_exception(True)
                coreapi.enable_authentication(True, "quick")
                coreapi.verify_expiry(True)
                coreapi.verify_age("18-120")
                coreapi.enable_dualside_check(True)
                
                response: dict = coreapi.scan(
                                    document_primary=payload.frontPage, 
                                    document_secondary=payload.backPage, 
                                    biometric_photo=payload.userFace)

                if response['authentication']['score'] < 0.5:
                    raise settings.DocumentNotAuthentic()                        

                if not response['face']['isIdentical']:
                    raise settings.FacesNotIdentical() 
                
                producer = AIOKafkaProducer(
                            loop=kafkaSettings.loop(), 
                            bootstrap_servers=kafkaSettings.KAFKA_BOOTSTRAP_SERVERS)
                await producer.start()
                try:
                    userIdJson = UserId.parse_obj(payload).json().encode("utf-8")
                    await producer.send_and_wait(
                            topic=kafkaSettings.USER_VERIFIED_TOPIC, 
                            value=userIdJson)
                finally:
                    await producer.stop()

            except idanalyzer.APIError as e:
                details = e.args[0]
                print("API error code: {}, message: {}".format(details["code"], details["message"]))
            except Exception as e:
                print(e)
    finally:
        await consumer.stop()



