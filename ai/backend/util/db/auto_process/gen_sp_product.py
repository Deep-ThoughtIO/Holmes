from ai.backend.util.db.auto_process.tools_sp_adGroup import AdGroupTools
from ai.backend.util.db.auto_process.tools_db_sp import DbSpTools
from ai.backend.util.db.auto_process.tools_db_new_sp import DbNewSpTools
from datetime import datetime
from ai.backend.util.db.auto_process.tools_sp_product import ProductTools


class Gen_product:
    def __init__(self,brand):
        self.brand = brand

# 创建/新增品
    def create_productsku(self,market,campaignId,adGroupId,sku,asin,state):
        product_info = {
      "productAds": [
        {
          "campaignId": str(campaignId),
          "state": state,
          "sku": sku,
          "asin": asin,
          "adGroupId": str(adGroupId)
        }
      ]
    }
        # 执行新增品 返回adId
        apitoolProduct=ProductTools(self.brand)
        adId = apitoolProduct.create_product_api(product_info,market)
        print(adId)

        # 如果执行成功或者失败 记录到log表记录
        dbNewTools = DbNewSpTools(self.brand,market)
        if adId[0]=="success":
            dbNewTools.create_sp_product(market,campaignId,asin,sku,adGroupId,adId[1],"success",datetime.now(),"SP")
        else:
            dbNewTools.create_sp_product(market,campaignId,asin,sku,adGroupId,adId[1],"failed",datetime.now(),"SP")
        return adId[1]
    # 新增测试
    # create_productsku('FR','284793893968513','B075SWSWHR','PAUSED','LPM17SS0035MT0300LR4','397527887041271')


    # 修改品的信息  - 暂时只能修改品的状态
    def update_product(self,market,adId,state):
        product_info = {
            "productAds": [
                {
                    "adId": adId,
                    "state": state
                }
            ]
        }
        # 执行修改品
        apitoolProduct = ProductTools(self.brand)
        adIdres = apitoolProduct.update_product_api(product_info,market)
        print(adIdres)
        # 如果执行成功或者失败 记录到log表记录
        dbNewTools = DbNewSpTools(self.brand,market)
        if adIdres[0] == "success":
            dbNewTools.update_sp_product(market, adId, state, "success", datetime.now())
        else:
            dbNewTools.update_sp_product(market, adId, state, "failed", datetime.now())

    #修改品测试
    # update_product('US','366708088753798','ENABLED')
