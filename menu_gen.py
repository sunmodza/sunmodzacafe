import json
from typing import Dict, List

from pip import main


def generate_variation(name, cost):
    variation = {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "text",
                "text": str(name),
                "contents": []
            },
            {
                "type": "text",
                "text": str(cost),
                "contents": []
            }
        ]
    }
    return variation


def generate_select_button(name, var_type, value):
    data = {
        "type": "button",
        "action": {
            "type": "message",
            "label": var_type,
            "text": f'{name} {var_type} {value}'
        }
    }
    return data


def gen_a_menu(name, img_uri, stars, describe, variations_price):
    # print(menu_data,"kkie")
    #name, img_uri, stars, describe , variations_price = menu_data

    variations_price_show = [generate_variation(
        i[0], i[1]) for i in variations_price]

    buttons = [generate_select_button(name, i[0], i[1])
               for i in variations_price]

    data = {
        "type": "bubble",
        "direction": "ltr",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#99EC51FF",
            "borderColor": "#FF0000FF",
            "contents": [
                {
                    "type": "text",
                    "text": name,
                    "size": "xxl",
                    "align": "center",
                    "contents": []
                }
            ]
        },
        "hero": {
            "type": "image",
            "url": img_uri,
            "size": "full",
            "aspectRatio": "1.51:1",
            "aspectMode": "fit"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "spacer"
                },
                {
                    "type": "text",
                    "text": "⭐"*stars,
                    "contents": []
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                              {
                                  "type": "text",
                                  "text": describe,
                                  "contents": []
                              }
                            ]
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                              {
                                  "type": "text",
                                  "text": "SIZE",
                                  "contents": []
                              },
                                {
                                  "type": "box",
                                  "layout": "vertical",
                                  "contents": variations_price_show
                              }
                            ]
                        }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": buttons
        }
    }

    return data


def gen_whole_menu(menus):
    # print(menus,"23232")
    # print(menus[0])
    menus = [gen_a_menu(*menu) for menu in menus]
    # print(menus[0])
    # return

    data = {
        "line": {
            "type": "flex",
            "altText": "Flex Message",
            "contents": {
                "type": "carousel",
                "contents": menus
            }
        }
    }

    return data


def gen_cart_a_content(name, variation, price, quantity):
    data = {
        "type": "box",
        "layout": "vertical",
        "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"{name}({quantity})",
                            "contents": []
                        },
                        {
                            "type": "text",
                            "text": str(variation),
                            "contents": []
                        },
                        {
                            "type": "text",
                            "text": str(price),
                            "contents": []
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": f"+",
                                "text": f"{name} {variation} {price}"
                            },
                            "gravity": "center"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": f"-",
                                "text": f"{name} {variation} min"
                            }
                        }
                    ]
                }
        ]
    }
    return data


def gen_cart(user_cart, total_price):

    user_cart = [gen_cart_a_content(name, variation, price, quantity) for (
        name, variation, price, quantity) in user_cart]
    data = {
        "payload": {
            "line": {
                "altText": "Flex Message",
                "contents": {
                    "direction": "ltr",
                    "body": {
                        "contents": user_cart,
                        "type": "box",
                        "layout": "vertical"
                    },
                    "header": {
                        "layout": "vertical",
                        "type": "box",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Cart",
                                "contents": [],
                                "align": "center"
                            }
                        ]
                    },
                    "type": "bubble",
                    "footer": {
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "label": f"Checkout {total_price}",
                                    "type": "message",
                                    "text": "Checkout"
                                }
                            }
                        ],
                        "type": "box"
                    }
                },
                "type": "flex"
            }
        }
    }
    return data


def gen_a_propic(name,img_uri,describe,order_this):
    data = {
        "type": "bubble",
        "direction": "ltr",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": name,
                    "align": "center",
                    "contents": []
                }
            ]
        },
        "hero": {
            "type": "image",
            "url": img_uri,
            "size": "full",
            "aspectRatio": "1.51:1",
            "aspectMode": "fit"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": describe,
                    "align": "center",
                    "contents": []
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "สั่งเลยดิ",
                        "text": order_this
                    }
                }
            ]
        }
    }
    return data


def gen_promo(promos):
  #print(promos)
  promos = [gen_a_propic(name,img_uri,describe,order_this) for [name,img_uri,describe,order_this] in promos]

  data = {"payload": {
      "line": {
          "type": "flex",
          "altText": "Flex Message",
          "contents": {
              "type": "carousel",
              "contents": promos
          }
      }
  }}
  return data


# gen_menus
if __name__ == "__main__":

    #a = gen_whole_menu([["sunmodza", "https://raw.githubusercontent.com/sunmodza/datbakery_vc/main/cake/cake11.jpg", 3, "GOOD", [["SMALL", 500], ["LARGE", 1000]]],["sunmodza2", "https://raw.githubusercontent.com/sunmodza/datbakery_vc/main/cake/cake11.jpg", 3, "GOOD", [["SMALL", 500], ["LARGE", 1000], ["SUPER", 1500]]]])
    # print(json.dumps(a))
    ab = gen_promo([[
      "sunmodza","https://raw.githubusercontent.com/sunmodza/datbakery_vc/main/cake/cake11.jpg","delight","เค้ก SMALL 500"
    ]])
    #ab = #gen_cart([["cake", "big", 50, 1], ["cake", "small", "50", 2]], 300)
    print(json.dumps(ab))
