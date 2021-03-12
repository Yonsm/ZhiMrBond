# [https://github.com/Yonsm/ZhiMrBond](https://github.com/Yonsm/ZhiMrBond)

MrBond Airer Component for HomeAssistant

邦先生晾衣架组件。目前仅验证了 `M1`/`M1 Pro` 型号可用，如果其它型号需要支持请给我[提 issue](https://github.com/Yonsm/ZhiMrBond/issues)。

## 1. 安装准备

把 `zhimrbond` 放入 `custom_components`；也支持在 [HACS](https://hacs.xyz/) 中添加自定义库的方式安装。

_依赖 [python-miio](https://github.com/rytilahti/python-miio)，运行时自动检查安装。_

## 2. 配置方法

参见 [我的 Home Assistant 配置](https://github.com/Yonsm/.homeassistant) 中 [configuration.yaml](https://github.com/Yonsm/.homeassistant/blob/main/configuration.yaml)

```yaml
zhimrbond:
  name: 晾衣架
  host: Airer
  token: !secret airer_token
```

以上配置会自动生成两个设备 `light.liang_yi_jia` 和 `cover.liang_yi_jia`。其中：

- `必选` `name` 可以自定义的设备名称
- `必选` `host` 可以是主机名或 IP 地址
- `必选` `token` 是 miio 设备的 token

_如何获取 `token`？_ 参见 [MiService](https://github.com/Yonsm/MiService)

## 2. 已知问题

分析`米家` APP 网络协议发现应该有晾衣架位置状态，但 `miot` [spec](http://miot-spec.org/miot-spec-v2/instance?type=urn:miot-spec-v2:device:airer:0000A00D:mrbond-m1pro:1) 和 `miio` 实测均无法获取真实状态，故初次运行可能无法获取准确状态，之后会记录上次操作后的假定位置。

## 3. 其它型号

其它型号没有测试，如果必要可以把型号[提 Issue](https://github.com/Yonsm/ZhiMrBond/issues) 给我。

```
micli.py spec mrbond
{
  "mrbond.airer.mrbond": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-mrbond:1",
  "mrbond.curtain.rac01": "urn:miot-spec-v2:device:curtain:0000A00C:mrbond-rac01:1",
  "mrbond.dryer.m2": "urn:miot-spec-v2:device:clothes-dryer:0000A06D:mrbond-m2:1",
  "mrbond.airer.m2": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-m2:1",
  "mrbond.airer.znlyj1": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-znlyj1:1",
  "mrbond.curtain.rac03": "urn:miot-spec-v2:device:curtain:0000A00C:mrbond-rac03:1",
  "mrbond.airer.m2pro": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-m2pro:1",
  "mrbond.dryer.hgja1": "urn:miot-spec-v2:device:clothes-dryer:0000A06D:mrbond-hgja1:1",
  "mrbond.airer.c1xpro": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-c1xpro:1",
  "mrbond.remote.yk1460": "urn:miot-spec-v2:device:remote-control:0000A021:mrbond-yk1460:1",
  "mrbond.airer.m1tpro": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-m1tpro:1",
  "mrbond.airer.m1t": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-m1t:1",
  "mrbond.airer.c1x": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-c1x:1",
  "mrbond.curtain.r1x": "urn:miot-spec-v2:device:curtain:0000A00C:mrbond-r1x:1:0000C817",
  "mrbond.airer.m31d": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-m31d:1",
  "mrbond.airer.m31c": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-m31c:1",
  "mrbond.airer.m31b": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-m31b:1",
  "mrbond.airer.m31a": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-m31a:1",
  "mrbond.airer.m53c": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-m53c:1",
  "mrbond.airer.m53pro": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-m53pro:1",
  "mrbond.airer.m33a": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-m33a:1",
  "mrbond.airer.m33c": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-m33c:1",
  "mrbond.airp.h1pro": "urn:miot-spec-v2:device:air-purifier:0000A007:mrbond-h1pro:1",
  "mrbond.airer.m1pro": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-m1pro:1",
  "mrbond.airer.m1s": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-m1s:1",
  "mrbond.airer.m1super": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-m1super:1",
  "mrbond.airer.m1": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-m1:1",
  "mrbond.airer.m0": "urn:miot-spec-v2:device:airer:0000A00D:mrbond-m0:1"
}
```

## 4. 参考

- [ZhiDash](https://github.com/Yonsm/ZhiDash)
- [Yonsm.NET](https://yonsm.github.io)
- [Hassbian.com](https://bbs.hassbian.com/thread-12336-1-1.html)
- [Yonsm's .homeassistant](https://github.com/Yonsm/.homeassistant)
