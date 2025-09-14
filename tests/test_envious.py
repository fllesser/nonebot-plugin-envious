async def test_envious_add_envious():
    from nonebot_plugin_envious import gem

    gem.add_envious("刘德华")
    gem.add_envious("刘德华")
    assert "刘德华" in gem.envious_list
    assert len(gem.envious_list) == len(gem.default_envious_list) + 1


async def test_envious_reset():
    from nonebot_plugin_envious import econfig, gem, reset_envious

    gem.add_envious("华为")
    gem.add_envious("koishi")
    gem.add_envious("刘德华")
    gem.add_envious("刘德华")
    assert len(gem.envious_list) == len(gem.default_envious_list) + 1
    assert "刘德华" in gem.envious_list
    assert "华为" in gem.envious_list
    assert "koishi" in gem.envious_list

    await reset_envious()
    assert gem.envious_list == econfig.envious_list

