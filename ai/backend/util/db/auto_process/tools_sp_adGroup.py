import os

import pymysql
from ad_api.api import sponsored_products
from ad_api.base import Marketplaces
import json
import datetime
from decimal import Decimal
from ai.backend.util.db.configuration.path import get_config_path
from ai.backend.util.db.util.common import get_ad_my_credentials,get_proxies


class AdGroupTools:
    def __init__(self,brand):
        self.brand = brand

    def load_credentials(self,market):
        my_credentials,access_token = get_ad_my_credentials(market,self.brand)
        return my_credentials,access_token


    # 新建广告组
    def create_adGroup_api(self,adGroup_info,market):
        try:
            credentials, access_token = self.load_credentials(market)
            result = sponsored_products.AdGroupsV3(credentials=credentials,
                                                   marketplace=Marketplaces[market.upper()],
                                                   access_token=access_token,
                                                   proxies=get_proxies(market),
                                                   debug=True).create_ad_groups(
                body=json.dumps(adGroup_info))
        except Exception as e:
            print("create adGroup failed: ", e)
            result = None
        adGroupID = ""
        if result and result.payload["adGroups"]["success"]:
            adGroupID = result.payload["adGroups"]["success"][0]["adGroup"]["adGroupId"]
            print("create adGroup success,adGroupId is:", adGroupID)
            return ["success",adGroupID]
        else:
            print("create adGroup failed:")
            return ["failed", adGroupID]


    # 更新广告组
    def update_adGroup_api(self,adGroup_info,market):
        credentials, access_token = self.load_credentials(market)
        try:
            result = sponsored_products.AdGroupsV3(credentials=credentials,
                                                   marketplace=Marketplaces[market.upper()],
                                                   access_token=access_token,
                                                   proxies=get_proxies(market),
                                                   debug=True).edit_ad_groups(
                body=json.dumps(adGroup_info))
        except Exception as e:
            print("update adGroup failed: ", e)
            result = None
        adGroupID = ""
        if result and result.payload["adGroups"]["success"]:
            adGroupID = result.payload["adGroups"]["success"][0]["adGroup"]["adGroupId"]
            print("update adGroup success,adGroupId is:", adGroupID)
            return ["success",adGroupID]
        else:
            print("update adGroup failed:", e)
            return ["failed", adGroupID]


    def get_adGroup_api(self,market,adGroupID):
        credentials, access_token = self.load_credentials(market)
        adGroup_info = {
  "maxResults": 10,
  "adGroupIdFilter": {
    "include": [
      str(adGroupID)
    ]
  },
  "includeExtendedDataFields": True,
}
        try:
            result = sponsored_products.AdGroupsV3(credentials=credentials,
                                                   marketplace=Marketplaces[market.upper()],
                                                   access_token=access_token,
                                                   proxies=get_proxies(market),
                                                   debug=True).list_ad_groups(
                body=json.dumps(adGroup_info))
        except Exception as e:
            print("查找广告组失败: ", e)
            result = None
        adGroupID = ""
        if result and result.payload["adGroups"][0]["defaultBid"]:
            defaultBid_old = result.payload["adGroups"][0]["defaultBid"]
            print("addgroup 查找广告组成功,adGroupId is:", adGroupID)
        else:
            print("查找广告组失败")
            defaultBid_old=1
        return defaultBid_old

    def get_adGroup_negativekw(self, market, adGroupID):
        credentials, access_token = self.load_credentials(market)
        adGroup_info = {
            "maxResults": 500,
            "adGroupIdFilter": {
                "include": [
                    str(adGroupID)
                ]
            },
            "includeExtendedDataFields": True,
        }
        try:
            result = sponsored_products.NegativeKeywordsV3(credentials=credentials,
                                                           marketplace=Marketplaces[market.upper()],
                                                           access_token=access_token,
                                                           proxies=get_proxies(market),
                                                           debug=True).list_negative_keywords(
                body=json.dumps(adGroup_info))
        except Exception as e:
            print("查找广告组否定关键词失败: ", e)
            result = None
        if result and result.payload["negativeKeywords"]:
            negativeKeywords = result.payload["negativeKeywords"]
            print("addgroup 查找广告组否定关键词成功")
        else:
            print("查找广告组失败:")
            negativeKeywords = None
        return negativeKeywords

    # 广告组增加否定定向关键词
    def add_adGroup_negativekw(self,adGroup_negativekw_info,market):
        try:
            credentials, access_token = self.load_credentials(market)
            result = sponsored_products.NegativeKeywordsV3(credentials=credentials,
                                                           marketplace=Marketplaces[market.upper()],
                                                           access_token=access_token,
                                                           proxies=get_proxies(market),
                                                           debug=True).create_negative_keyword(
                body=json.dumps(adGroup_negativekw_info))
        except Exception as e:
            print("add adGroup negative keyword failed: ", e)
            result = None
        if result and result.payload["negativeKeywords"]["success"][0]["negativeKeywordId"]:
            negativeKeywordId = result.payload["negativeKeywords"]["success"][0]["negativeKeywordId"]
            print("add adGroup negative keyword success,negativeKeywordId is:", negativeKeywordId)
            return ["success",negativeKeywordId]
        else:
            print("add adGroup negative keyword failed:")
            return ["failed", ""]

    # 广告组修改否定定向关键词
    def update_adGroup_negativekw(self,adGroup_negativekw_info):
        try:
            result = sponsored_products.NegativeKeywordsV3(credentials=my_credentials,
                                                            marketplace=Marketplaces.NA,
                                                            debug=True).edit_negative_keyword(
                body=json.dumps(adGroup_negativekw_info))
        except Exception as e:
            print("update adGroup negative keyword failed: ", e)
            result = None
        if result and result.payload["negativeKeywords"]["success"]:
            negativeKeywordId = result.payload["negativeKeywords"]["success"][0]["negativeKeywordId"]
            print("update adGroup negative keyword success,negativeKeywordId is:", negativeKeywordId)
            return ["success",negativeKeywordId]
        else:
            print("update adGroup negative keyword failed:", e)
            return ["failed", ""]

    #
    def list_adGroup_negative_pd(self, adGroup_negativekw_info, market):
        try:
            credentials, access_token = self.load_credentials(market)
            result = sponsored_products.NegativeTargetsV3(credentials=credentials,
                                                          marketplace=Marketplaces[market.upper()],
                                                          access_token=access_token,
                                                          proxies=get_proxies(market),
                                                          debug=True).list_negative_product_targets(
                body=json.dumps(adGroup_negativekw_info))
        except Exception as e:
            print("list adGroup negative product failed: ", e)
            result = None
        if result:
            print("list adGroup negative product success")
            return ["success", result]
        # if result and result.payload["negativeKeywords"]["success"]:
        #     negativeKeywordId = result.payload["negativeKeywords"]["success"][0]["negativeKeywordId"]
        #     print("add adGroup negative keyword success,negativeKeywordId is:", negativeKeywordId)
        #     return ["success", negativeKeywordId]
        else:
            print("list adGroup negative product failed:", e)
            return ["failed", ""]

    def list_adGroup_TargetingClause(self, adGroupID, market):
        try:
            credentials, access_token = self.load_credentials(market)
            # print(f'credentials:{credentials}')
            # print(f'access_token:{access_token}')
            adGroup_info = {
                "adGroupIdFilter": {
                    "include": [
                        str(adGroupID)
                    ]
                }
            }
            result = sponsored_products.TargetsV3(credentials=credentials,
                                                  marketplace=Marketplaces[market.upper()],
                                                  access_token=access_token,
                                                  proxies=get_proxies(market),
                                                  debug=True).list_product_targets(
                body=json.dumps(adGroup_info))
        except Exception as e:
            print("list adGroup TargetingClause failed: ", e)
            result = None
        if result and result.payload["targetingClauses"]:
            print("list adGroup TargetingClause success")
            return result.payload["targetingClauses"]
        # if result and result.payload["negativeKeywords"]["success"]:
        #     negativeKeywordId = result.payload["negativeKeywords"]["success"][0]["negativeKeywordId"]
        #     print("add adGroup negative keyword success,negativeKeywordId is:", negativeKeywordId)
        #     return ["success", negativeKeywordId]
        else:
            print("list adGroup TargetingClause failed")
            return result.payload["targetingClauses"]

    def list_adGroup_TargetingClause_by_campaignId(self, campaignId, market):
        try:
            credentials, access_token = self.load_credentials(market)
            adGroup_info = {
                "campaignIdFilter": {
                    "include": [
                        str(campaignId)
                    ]
                }
            }
            result = sponsored_products.TargetsV3(credentials=credentials,
                                                  marketplace=Marketplaces[market.upper()],
                                                  access_token=access_token,
                                                  proxies=get_proxies(market),
                                                  debug=True).list_product_targets(
                body=json.dumps(adGroup_info))
        except Exception as e:
            print("list adGroup TargetingClause failed: ", e)
            result = None
        if result and result.payload["targetingClauses"]:
            print("list adGroup TargetingClause success")
            return result.payload["targetingClauses"]
        # if result and result.payload["negativeKeywords"]["success"]:
        #     negativeKeywordId = result.payload["negativeKeywords"]["success"][0]["negativeKeywordId"]
        #     print("add adGroup negative keyword success,negativeKeywordId is:", negativeKeywordId)
        #     return ["success", negativeKeywordId]
        else:
            print("list adGroup TargetingClause failed")
            return result.payload["targetingClauses"]

    def list_adGroup_TargetingClause_by_targetId(self, targetId, market):
        try:
            credentials, access_token = self.load_credentials(market)
            adGroup_info = {
                "targetIdFilter": {
                    "include": [
                        str(targetId)
                    ]
                }
            }
            result = sponsored_products.TargetsV3(credentials=credentials,
                                                  marketplace=Marketplaces[market.upper()],
                                                  access_token=access_token,
                                                  proxies=get_proxies(market),
                                                  debug=True).list_product_targets(
                body=json.dumps(adGroup_info))
        except Exception as e:
            print("list adGroup TargetingClause failed: ", e)
            result = None
        if result and result.payload["targetingClauses"]:
            print("list adGroup TargetingClause success")
            return result.payload["targetingClauses"]
        # if result and result.payload["negativeKeywords"]["success"]:
        #     negativeKeywordId = result.payload["negativeKeywords"]["success"][0]["negativeKeywordId"]
        #     print("add adGroup negative keyword success,negativeKeywordId is:", negativeKeywordId)
        #     return ["success", negativeKeywordId]
        else:
            print("list adGroup TargetingClause failed")
            return result.payload["targetingClauses"]

    def update_adGroup_TargetingC(self, adGroup_info, market):
        try:
            credentials, access_token = self.load_credentials(market)
            result = sponsored_products.TargetsV3(credentials=credentials,
                                                  marketplace=Marketplaces[market.upper()],
                                                  access_token=access_token,
                                                  proxies=get_proxies(market),
                                                  debug=True).edit_product_targets(
                body=json.dumps(adGroup_info))
        except Exception as e:
            print("update adGroup TargetingClause failed: ", e)
            result = None
        if result and result.payload["targetingClauses"]["success"]:
            print("update adGroup TargetingClause success")
            return ["success", result.payload["targetingClauses"]["success"][0]]
        # if result and result.payload["negativeKeywords"]["success"]:
        #     negativeKeywordId = result.payload["negativeKeywords"]["success"][0]["negativeKeywordId"]
        #     print("add adGroup negative keyword success,negativeKeywordId is:", negativeKeywordId)
        #     return ["success", negativeKeywordId]
        else:
            print("update adGroup TargetingClause failed")
            return ["failed", ""]

    def create_adGroup_TargetingC(self, adGroup_info, market):
        try:
            credentials, access_token = self.load_credentials(market)
            result = sponsored_products.TargetsV3(credentials=credentials,
                                                  marketplace=Marketplaces[market.upper()],
                                                  access_token=access_token,
                                                  proxies=get_proxies(market),
                                                  debug=True).create_product_targets(
                body=json.dumps(adGroup_info))
        except Exception as e:
            print("create adGroup TargetingClause failed: ", e)
            result = None
        if result and result.payload["targetingClauses"]["success"]:
            print("create adGroup TargetingClause success")
            return ["success", result.payload["targetingClauses"]["success"][0]]
        # if result and result.payload["negativeKeywords"]["success"]:
        #     negativeKeywordId = result.payload["negativeKeywords"]["success"][0]["negativeKeywordId"]
        #     print("add adGroup negative keyword success,negativeKeywordId is:", negativeKeywordId)
        #     return ["success", negativeKeywordId]
        else:
            print("create adGroup TargetingClause failed")
            return ["failed", ""]



    def list_adGroup_Targetingrecommendations(self, market, asins):
        adGroup_info={
  "asins": asins,
  "includeAncestor": False
}
        try:
            credentials, access_token = self.load_credentials(market)

            result = sponsored_products.TargetsV3(credentials=credentials,
                                                  marketplace=Marketplaces[market.upper()],
                                                  access_token=access_token,
                                                  proxies=get_proxies(market),
                                                  debug=True).list_products_targets_categories_recommendations(
                body=json.dumps(adGroup_info))
        except Exception as e:
            print("list adGroup Targetingrecommendations failed: ", e)
            result = None
        if result and result.payload:
            print("list adGroup Targetingrecommendations success")
            return result.payload
        # if result and result.payload["negativeKeywords"]["success"]:
        #     negativeKeywordId = result.payload["negativeKeywords"]["success"][0]["negativeKeywordId"]
        #     print("add adGroup negative keyword success,negativeKeywordId is:", negativeKeywordId)
        #     return ["success", negativeKeywordId]
        else:
            print("list adGroup Targetingrecommendations failed")
            return ["failed", ""]


    def list_category_refinements(self, market, categoryId):
        try:
            credentials, access_token = self.load_credentials(market)

            result = sponsored_products.TargetsV3(credentials=credentials,
                                                  marketplace=Marketplaces[market.upper()],
                                                  access_token=access_token,
                                                  proxies=get_proxies(market),
                                                  debug=True).list_products_targets_category_refinements(
                categoryId=categoryId)
        except Exception as e:
            print("list category_refinements failed: ", e)
            result = None
        if result and result.payload:
            print("list category_refinements success")
            return result.payload
        # if result and result.payload["negativeKeywords"]["success"]:
        #     negativeKeywordId = result.payload["negativeKeywords"]["success"][0]["negativeKeywordId"]
        #     print("add adGroup negative keyword success,negativeKeywordId is:", negativeKeywordId)
        #     return ["success", negativeKeywordId]
        else:
            print("list category_refinements failed")
            return ["failed", ""]


    def list_category_bid_recommendations(self, market, categoryId,new_campaign_id,new_adgroup_id):
        adGroup_info={
  "targetingExpressions": [
    {
      "type": "PAT_CATEGORY",
      "value": str(categoryId)
    }
  ],
  "campaignId": new_campaign_id,
  "recommendationType": "BIDS_FOR_EXISTING_AD_GROUP",
  "adGroupId": new_adgroup_id
}
        try:
            credentials, access_token = self.load_credentials(market)

            result = sponsored_products.BidRecommendationsV3(credentials=credentials,
                                                             marketplace=Marketplaces[market.upper()],
                                                             access_token=access_token,
                                                             proxies=get_proxies(market),
                                                             debug=True).get_bid_recommendations(
                body=json.dumps(adGroup_info))
        except Exception as e:
            print("list category_bid failed: ", e)
            result = None
        if result and result.payload:
            print("list category_bid success")
            return result.payload
        # if result and result.payload["negativeKeywords"]["success"]:
        #     negativeKeywordId = result.payload["negativeKeywords"]["success"][0]["negativeKeywordId"]
        #     print("add adGroup negative keyword success,negativeKeywordId is:", negativeKeywordId)
        #     return ["success", negativeKeywordId]
        else:
            print("list category_bid failed")
            return ["failed", ""]

    def list_product_bid_recommendations(self, market, asin,new_campaign_id,new_adgroup_id):
        adGroup_info={
  "targetingExpressions": [
    {
      "type": "PAT_ASIN",
      "value": asin
    }
  ],
  "campaignId": new_campaign_id,
  "recommendationType": "BIDS_FOR_EXISTING_AD_GROUP",
  "adGroupId": new_adgroup_id
}
        try:
            credentials, access_token = self.load_credentials(market)

            result = sponsored_products.BidRecommendationsV3(credentials=credentials,
                                                             marketplace=Marketplaces[market.upper()],
                                                             access_token=access_token,
                                                             proxies=get_proxies(market),
                                                             debug=True).get_bid_recommendations(
                body=json.dumps(adGroup_info))
        except Exception as e:
            print("list product_bid failed: ", e)
            result = None
        if result and result.payload:
            print("list product_bid success")
            return result.payload
        # if result and result.payload["negativeKeywords"]["success"]:
        #     negativeKeywordId = result.payload["negativeKeywords"]["success"][0]["negativeKeywordId"]
        #     print("add adGroup negative keyword success,negativeKeywordId is:", negativeKeywordId)
        #     return ["success", negativeKeywordId]
        else:
            print("list product_bid failed")
            return ["failed", ""]

    def list_automatic_targeting_bid_recommendations(self, market, new_campaign_id, new_adgroup_id):
        adGroup_info = {
            "targetingExpressions": [
                {
                "type": "CLOSE_MATCH"
                },
                {
                "type": "LOOSE_MATCH"
                },
                {
                "type": "SUBSTITUTES"
                },
                {
                "type": "COMPLEMENTS"
                }
            ],
            "campaignId": new_campaign_id,
            "recommendationType": "BIDS_FOR_EXISTING_AD_GROUP",
            "adGroupId": new_adgroup_id
        }
        try:
            credentials, access_token = self.load_credentials(market)

            result = sponsored_products.BidRecommendationsV3(credentials=credentials,
                                                             marketplace=Marketplaces[market.upper()],
                                                             access_token=access_token,
                                                             proxies=get_proxies(market),
                                                             debug=True).get_bid_recommendations(
                body=json.dumps(adGroup_info))
        except Exception as e:
            print("list product_bid failed: ", e)
            result = None
        if result and result.payload:
            print("list product_bid success")
            return result.payload
        # if result and result.payload["negativeKeywords"]["success"]:
        #     negativeKeywordId = result.payload["negativeKeywords"]["success"][0]["negativeKeywordId"]
        #     print("add adGroup negative keyword success,negativeKeywordId is:", negativeKeywordId)
        #     return ["success", negativeKeywordId]
        else:
            print("list product_bid failed")
            return ["failed", ""]

    def create_adGroup_Negative_TargetingClauses(self, adGroup_info, market):
        try:
            credentials, access_token = self.load_credentials(market)
            result = sponsored_products.NegativeTargetsV3(credentials=credentials,
                                                  marketplace=Marketplaces[market.upper()],
                                                  access_token=access_token,
                                                  proxies=get_proxies(market),
                                                  debug=True).create_negative_product_targets(
                body=json.dumps(adGroup_info))
        except Exception as e:
            print("create adGroup Negative TargetingClauses failed: ", e)
            result = None
        if result and result.payload["negativeTargetingClauses"]["success"]:
            print("create adGroup Negative TargetingClauses success")
            return ["success", result.payload["negativeTargetingClauses"]["success"][0]]
        # if result and result.payload["negativeKeywords"]["success"]:
        #     negativeKeywordId = result.payload["negativeKeywords"]["success"][0]["negativeKeywordId"]
        #     print("add adGroup negative keyword success,negativeKeywordId is:", negativeKeywordId)
        #     return ["success", negativeKeywordId]
        else:
            print("create adGroup Negative TargetingClause failed")
            return ["failed", ""]

    def list_category(self, market):
        try:
            credentials, access_token = self.load_credentials(market)

            result = sponsored_products.TargetsV3(credentials=credentials,
                                                  marketplace=Marketplaces[market.upper()],
                                                  access_token=access_token,
                                                  proxies=get_proxies(market),
                                                  debug=True).list_targets_categories(

            )
        except Exception as e:
            print("list category failed: ", e)
            result = None
        if result and result.payload:
            print("list category success")
            return result.payload['CategoryTree']
        # if result and result.payload["negativeKeywords"]["success"]:
        #     negativeKeywordId = result.payload["negativeKeywords"]["success"][0]["negativeKeywordId"]
        #     print("add adGroup negative keyword success,negativeKeywordId is:", negativeKeywordId)
        #     return ["success", negativeKeywordId]
        else:
            print("list category_refinements failed")
            return ["failed", ""]
# 广告组更新否定关键词测试
# adGroup_negativekw_info = {
# "negativeKeywords": [
# {
# "keywordId": "426879824500654",
# "state": "ENABLED"
# }
# ]
# }
# agt=AdGroupTools_SD()
# res = agt.get_adGroup_negativekw('FR',306913253726907)
# print(type(res))
# print(res)

# 新增广告组否定定向关键词测试 --426879824500654
# adGroup_negativekw_info = {
#   "negativeKeywords": [
#     {
#       "campaignId": "531571979684792",
#       "matchType": "NEGATIVE_EXACT",
#       "state": "ENABLED",
#       "adGroupId": "311043566627712",
#       "keywordText": "0508negativekw01"
#     }
#   ]
# }


# agt = AdGroupTools()
# res = agt.list_adGroup_TargetingClause(48743010222967,'DE')
# # print(type(res))
# print(res)

# 测试
# adgroup_info={
#   "adGroups": [
#     {
#       "name": "adgroupB09ZQLY99J",
#       "state": "PAUSED",
#       "adGroupId": "311043566627712",
#       "defaultBid": 1.0
#     }
#   ]
# }
# #
# agt=AdGroupTools('KAPEYDESI')
# # 测试更新广告系列信息
# res = agt.get_adGroup_api('UK','560403892575481')
# #res = agt.list_adGroup_TargetingClause('479266699513385','UK')
# #res = agt.list_adGroup_Targetingrecommendations('FR',['B08NDYCFVG','B0CHRX765S','B0CHRYCWPG','B08NDY9F91','B08NDR42XX','B0CHRTK8LZ'])
# #res = agt.list_category_refinements('FR',464943031)464867031
# #res = agt.list_product_bid_recommendations('FR','B07L8GX9YY',332826141768516,366375831366135)
# #res = agt.list_category_bid_recommendations('FR',464867031,19768705031,332826141768516,366375831366135)
# #res = agt.list_adGroup_TargetingClause(366375831366135,'FR')
# # print(type(res))
# print(res)
# with open('output.txt', 'w', encoding='utf-8') as file:
#     # 将 res 转换为字符串并写入文件
#     file.write(str(res))
#
# print('结果已保存到 output.txt')