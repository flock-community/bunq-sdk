# from src.api import READ_UserEndpoint
# from src.api import CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint
# from src.api import RequestInquiry
#
# from src.client import Client
# from src.context import Context
#
# from src.wirespec import Serialization
#
# USER_API_KEY = "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95"
# service_name='PeterScript'
#
# serialization = Serialization()
# api = Client(serialization)
#
# context = Context(USER_API_KEY, service_name)
#
# def READ_User():
#     req = READ_UserEndpoint.Request(
#         itemId = context.user_id,
#         CacheControl = None,
#         UserAgent = context.service_name,
#         XBunqLanguage = None,
#         XBunqRegion = None,
#         XBunqClientRequestId = None,
#         XBunqGeolocation = None,
#         XBunqClientAuthentication = context.session_token,
#     )
#
#     res = api.READ_User(req)
#
#     match res:
#         case READ_UserEndpoint.Response200(body):
#             if body.UserPerson is None:
#                 raise Exception("User not found")
#             print(body.UserPerson.display_name)
#
# def CREATE_RequestInquiry_for_User_MonetaryAccount():
#     body = RequestInquiry(
#         amount_inquired = None,
#         counterparty_alias = None,
#         description = None,
#         attachment = None,
#         merchant_reference = None,
#         status = None,
#         minimum_age = None,
#         require_address = None,
#         want_tip = None,
#         allow_amount_lower = None,
#         allow_amount_higher = None,
#         allow_bunqme = False,
#         redirect_url = None,
#         event_id = None,
#         id = None,
#         created = None,
#         updated = None,
#         time_responded = None,
#         time_expiry = None,
#         monetary_account_id = None,
#         amount_responded = None,
#         user_alias_created = None,
#         user_alias_revoked = None,
#         batch_id = None,
#         scheduled_id = None,
#         bunqme_share_url = None,
#         address_shipping = None,
#         address_billing = None,
#         geolocation = None,
#         reference_split_the_bill = None
#     )
#
#     req = CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Request(
#         userID = context.user_id,
#         monetaryaccountID = 1,
#         CacheControl = None,
#         UserAgent = context.service_name,
#         XBunqLanguage = None,
#         XBunqRegion = None,
#         XBunqClientRequestId = None,
#         XBunqGeolocation = None,
#         XBunqClientAuthentication = context.session_token,
#         body=body
#     )
#
#     res = api.CREATE_RequestInquiry_for_User_MonetaryAccount(req)
#
#     match res:
#         case READ_UserEndpoint.Response200(body):
#             if body.UserPerson is None:
#                 raise Exception("User not found")
#             print(body.UserPerson.display_name)
#
# READ_User()
# CREATE_RequestInquiry_for_User_MonetaryAccount()