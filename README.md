# Yacamim
_Yacamim_ is a [Gemini](https://geminiprotocol.net) browser. Currently, it is only available as a Command-Line Application, but in the near future, a desktop application for Linux will be launched.

### Gemini Protocol
I could try to describe the project in a few words, but luckily, the Gemini developers have already done that, so let me quote them:

> 'Gemini is a new internet technology supporting an electronic library of interconnected text documents. That's not a new idea, but it's
not old-fashioned either. It's timeless and deserves tools that treat it as a first-class concept, not a vestigial corner case. Gemini isn't
about innovation or disruption; it's about providing respite for those who feel the internet has been disrupted enough already. We're not out
to change the world or destroy other technologies. We aim to build a lightweight online space where documents are just documents, in the interests
of every reader's privacy, attention, and bandwidth.'

I kind of fell in love with the idea of a simplistic internet environment, without all those shiny apps and ads all over the place. 
Gemini has become my go-to place to discover new blogs and navigate between documents.
### CLI Version (Currently available)
It's a basic implementation in Python, designed to better understand how I can connect to the internet via the Gemini protocol. It's not 
supposed to be used on a daily basis, but if you like the vintage vibe that comes from using the terminal to surf the internet, go ahead! 
I'll add some improvements to make this experience even better for you all.

### GUI Version (Future release)
That's the main application. I'm looking to develop the 'backend' in Lua and the 'frontend' in GTK-rs. It's a really complex project, and it 
might take a few months to get a working prototype, so I won't set a target release date (sorry).

### Mobile Version (In our roadmap)
It's not discarded, but also somewhat far-fetched for now. I aim to develop the GUI version first and then take a look at that.

### More Details
Visit [Gemini Specifications](https://geminiprotocol.net/docs/specification.gmi) to get more details over the implementation of this software.

### Usage
Yacamim uses [Poetry]() to manage its dependecies, so we recommend to install it.
Initially, you will need to clone the project:
```bash
git clone https://github.com/thigcampos/yacamim.git
```

Then, install the project using `poetry`:
```bash
poetry install
```

And, finally, run the `yacamim` command:
```bash
poetry run yacamim
```
