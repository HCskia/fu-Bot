import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBot_V11_Adapter

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(OneBot_V11_Adapter)

nonebot.load_from_toml("pyproject.toml")
nonebot.load_plugins("src\plugins\maimai")

if __name__ == "__main__":
    nonebot.run()