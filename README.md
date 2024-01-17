# aiograf

Безопасная библиотека на базе aiogram\pyrogram\aiocryptopay
- Исключает большенство исключений
- Добавляет новое FSM хранилище DillStorage
- Добавляет исполнитель длинных запросов для [@CryptoBot](https://t.me/CryptoBot)

Если у вас есть вопросы, пишите мне в телеграмме
[@static_assert](https://t.me/static_assert)

## Оглавление
- [Installation](#installation)
- [Example](https://github.com/iassert/aiograf_example.git)

<a name="installation"></a>
## Installation
* instruction for Ubuntu20

- Download Python3.10
```sh
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10
python3.10 --version
```

- Download [telegram-bot-api](https://github.com/tdlib/telegram-bot-api#dependencies)
```sh
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install make git zlib1g-dev libssl-dev gperf cmake clang-10 libc++-dev libc++abi-dev
git clone --recursive https://github.com/tdlib/telegram-bot-api.git
cd telegram-bot-api
rm -rf build
mkdir build
cd build
CXXFLAGS="-stdlib=libc++" CC=/usr/bin/clang-10 CXX=/usr/bin/clang++-10 cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=.. ..
cmake --build . --target install
cd ../..
ls -l telegram-bot-api/bin/telegram-bot-api*
```

- Download a project
```sh
git clone --recursive https://github.com/iassert/aiograf.git
```

- Install python lib
```sh
pip install -r requirements.txt
```
