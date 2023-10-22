<div align="center">

[![Maintainer](https://img.shields.io/badge/Maintainer-chr3st5an-purple?style=for-the-badge)](https://github.com/chr3st5an)
[![Python](https://img.shields.io/badge/Python->=3.8.1-blue?style=for-the-badge&logo=python)](https://www.python.org/downloads/)
[![Category](https://img.shields.io/badge/Category-OSINT-brightgreen?style=for-the-badge)](https://en.wikipedia.org/wiki/Open-source_intelligence)
[![License](https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge)](https://github.com/chr3st5an/tracer/blob/main/LICENSE)
![Version](https://img.shields.io/badge/Version-1.0.2-brightgreen?style=for-the-badge)
[![Logo](https://i.imgur.com/HV5KtwO.png)](https://github.com/chr3st5an/tracer)

### Tracer

Tracer detects on which website a username is currently in use!

**[Official Repository](https://github.com/chr3st5an/tracer)** · **[Report Bug](https://github.com/chr3st5an/tracer/issues)**

</div>

<br/>

## Features

---

Tracer provides the following features:

- 170+ sites that are checked

- Filter websites based on their domain or category

  - Limit the pool of sites that will be checked

- Browser version (GUI)

- Save the result of each check in a report file

- Open successful results in your browser

- Customizability:

  - Use the included config file to change the behavior of Tracer

- Easy to use

<div align="right">

[(Beam me up)](#tracer)

</div>

<br/>

## Built With

---

- ![aiohttp](https://img.shields.io/badge/aiohttp-black?style=for-the-badge&logo=aiohttp)

- ![jinja](https://img.shields.io/badge/jinja-black?style=for-the-badge&logo=jinja)

</br>

## Getting Started

---

### Prerequisites

For Tracer to work, you will need Python 3.7 or later and pip. You can download Python from the [official website](https://www.python.org/downloads/). Python ships with pip. Verify the versions:

- python

```bash
python -V
```

- pip

```bash
pip -V # or "python -m pip -V"
```

<div align="right">

[(Beam me up)](#tracer)

</div>

### Installation

1. Clone this repository

```bash
git clone https://github.com/chr3st5an/tracer.git
```

> 🛈 If you do not have `git`, you can download this repository by clicking on `Code` > `Download ZIP`. Unzip the folder and open a terminal.

2. Navigate into the just downloaded folder

```bash
cd tracer/
```

3. Install dependencies

```bash
pip install -r ./requirements.txt
```

<div align="right">

[(Beam me up)](#tracer)

</div>

<br/>

## Usage

---

After you installed all dependencies you are ready to run Tracer for the first time 🎉 To do so, open a terminal in the project's root folder and run the following command:

```bash
python tracer [OPTIONS] username
```

Where `[OPTIONS]` are optional flags you can pass to Tracer to modify its behavior. More about options [later](#options).

<div align="right">

[(Beam me up)](#tracer)

</div>

<br/>

## GUI

---

Tracer also offers a GUI in form of a webapp. You can run the webapp by executing the following command:

```bash
python tracer --web tracer
```

This will run the webapp on port 12345. Tracer should automatically open your browser and connect to the webapp. If not, open your browser manually and type `http://127.0.0.1:12345` into the search bar and hit enter.

![Browser](https://i.imgur.com/TRRtQMP.png)

<div align="right">

[(Beam me up)](#tracer)

</div>

<br/>

## Options

---

For a list of all available commands and options, use the `-h` flag or read the following section

```bash
python tracer -h
```

<details>

<summary>Options</summary>

- `-h`, `--help` *print a help message and exit*

- `-t <timeout>` *set a timeout for requests*

- `-e <domain>` *exclude a domain*

- `-o <domain>` *only check this domain for the username*

- `-O <category>` *only check sites that fall under this category for the username*

- `-E <category>` *exclude all sites that fall under this category*

- `-b` *open sites on which the username got found, in your default browser*

- `-v` *print additional information while the program runs*

- `-a` *print all websites*

- `--web` *run a GUI in form of a local webapp*

- `--ip-check` *retrieve your public IP address before starting the main program*

</details>

<div align="right">

[(Beam me up)](#tracer)

</div>

<br/>

## License

---

This project is licensed under the **MIT** license. For more information check out the project's license file.

<div align="right">

[(Beam me up)](#tracer)

</div>

<br/>

<div align="center">
    <a href="https://www.buymeacoffee.com/chr3st5an" target="_blank">
        <img src="https://cdn.buymeacoffee.com/buttons/v2/default-violet.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;"/>
    </a>
</div>
