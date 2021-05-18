# hltv-utility-api

![AutoParser](https://github.com/hx-w/hltv-utility-api/workflows/AutoParser/badge.svg)
![CodeAnalysis](https://github.com/hx-w/hltv-utility-api/workflows/CodeAnalysis/badge.svg)

Auto download and parse recent [hltv](https://hltv.org) demos to get **pro utility records**

## Build

### OS
`Ubuntu 20.04LTS`

### Golang

`sudo apt install golang-go`

Use `go version` to check version: `1.13.8 linux/amd64`

We need go version higher than `go 1.11`

### Demoinfocs-golang

Install [demoinfocs-golang](https://github.com/markus-wa/demoinfocs-golang)

`go get -u github.com/markus-wa/demoinfocs-golang/v2/pkg/demoinfocs`

> If your network is in CN, you may change Golang's proxy
>
> `go env -w GOPROXY=https://goproxy.cn,direct`

## API Format

### Match Info Index

GET: `/<mapname>` 

> get recent matches information index.

- [x] [`/de_dust2`](https://api.hx-w.top/de_dust2)
- [x] [`/de_mirage`](https://api.hx-w.top/de_mirage)
- [x] [`/de_inferno`](https://api.hx-w.top/de_inferno)
- [x] [`/de_train`](https://api.hx-w.top/de_train)
- [x] [`/de_overpass`](https://api.hx-w.top/de_overpass)
- [x] [`/de_nuke`](https://api.hx-w.top/de_nuke)
- [x] [`/de_vertigo`](https://api.hx-w.top/de_vertigo)
- [x] [`/de_ancient`](https://api.hx-w.top/de_ancient)

```json
[
  {
    "event": "Flashpoint 3",
    "maxround": "26",
    "time": "2021-05-11 05:51:51",
    "team1": { "name": "Astralis", "result": 2 },
    "team2": { "name": "OG", "result": 0 },
    "matchId": "2348420"
  }
]
```

### Match Info Detail

GET: `/<mapname>/<matchId>` 

> Get match utility records' detail from `matchId`

etc.

[`/de_inferno/2348420`](https://api.hx-w.top/de_inferno/2348420)

```json
[
    datapack,
    datapack
]
```

> default tickrate=128

#### datapack format

| Index | remark           | type    |
| ----- | ---------------- | ------- |
| 0     | aim_pitch        | float32 |
| 1     | aim_yaw          | float32 |
| 2     | air_time         | float32 |
| 3     | end_x            | float32 |
| 4     | end_y            | float32 |
| 5     | end_z            | float32 |
| 6     | is_duck          | bool    |
| 7     | is_jump          | bool    |
| 8     | is_walk          | bool    |
| 9     | round            | int     |
| 10    | round_throw_time | float   |
| 11    | nickname         | string  |
| 12    | steamid          | string  |
| 13    | teamname         | string  |
| 14    | throw_x          | float32 |
| 15    | throw_y          | float32 |
| 16    | throw_z          | float32 |
| 17    | utility_type     | string  |
| 18    | velocity_x       | float32 |
| 19    | velocity_y       | float32 |
| 20    | velocity_z       | float32 |
| 21    | entity_x         | float32 |
| 22    | entity_y         | float32 |
| 23    | entity_z         | float32 |

#### utility type enum

- `smokegrenade`
- `flashbang`
- `molotov`
- `incgrenade`
- `hegrenade`