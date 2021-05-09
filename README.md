# hltv-utility-api

Auto download and parse recent [hltv](https://hltv.org) demos to get **pro utility records**

## Installation

[TODO]

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


## Methods

1. `/getMatches`
2. `/getUtlityListByMatchId/<str: matchId>`
3. `/getUtilityRecordByUtilityId/<str: UtilityId>`

[TODO]
