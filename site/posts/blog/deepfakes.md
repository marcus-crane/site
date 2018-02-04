Title: deepfakes
Date: January 30, 2017

**While I believe this subject is important, do note that it is NSFW as the technology/community discussed are tightly tied to pornography**

## An overview

Just under a week ago, an article from The Verge titled [Fake celebrity porn is blowing up on Reddit, thanks to artificial intelligence](https://www.theverge.com/2018/1/24/16929148/fake-celebrity-porn-ai-deepfake-face-swapping-artificial-intelligence-reddit) was posted on [Hacker News](https://news.ycombinator.com/item?id=16226495). If you'd just glimpsed the headline, you might assume it's a bunch of shitstirrers up to no good with Photoshop but unfortunately, it's arguably worse.

The emergent field of machine learning had been mainly relegated to the realm of computer science due to the inherent complexity. As time marched on, new tools and libraries have popped up that make machine learning earlier than ever to dive into for professionals and hobbyists a-like. It was only a matter of time before someone decided to apply this to more taboo subjects and now we can see the results in this "fake" pornography. Now, I say "fake" to denote that it isn't "real" but often the results can be indistinguishable from reality itself making the term almost meaningless.

It isn't exactly hard to see where this can go wrong but after discussing this topic with a few non-technical coworkers, they seemed to have missed the forest for the trees. Their responses typically focused on the "cool tech" rather than realising that this is perhaps *the* Pandora's box which we can't go back from.

Given my feelings of "Oh fuck", this is my attempt at rounding up both my own thoughts and those pitches in various discussion threads I've seen because there's all sorts of ways this can go wrong. Before we begin, I should explain a bit more about this technology and how it works. This isn't a master class on machine learning by any means. It's designed to be ["as simple as possible, but not simpler"](https://quoteinvestigator.com/2011/05/13/einstein-simple/), mainly because my understanding of the concepts involved is surface level at best. For anything deeper, you should seek out other sources.

## What are deepfakes and how are they made?

[deepfakes](https://reddit.com/u/deepfakes) is the name of a user on reddit who "pioneered" this new wave of computer-generated celebrity pornography. To further promote discussion, and share the generated works, a subreddit called [/r/deepfakes](https://reddit.com/r/deepfakes) was created in his name. The term *deepfake* has since been coined to refer to the creations that followed and it's the term I'll be using going forward.

Just the term "Machine Learning" itself might invoke visions of [Skynet](https://en.wikipedia.org/wiki/Skynet_(Terminator)) but they aren't truly conscious in the way that you or I are. You're likely thinking, "How can a machine learn?" then if it isn't conscious. At its simplest, learning is taking a series of inputs (sound, sight, touch) and producing an output. When you first meet someone, you may forget their face but over time, you learn to recognise it. As time progresses, you can also identify them in different contexts such as an office, an airport or at a beach. In a rough sense, what's happening is that you're training your brain to identify their facial features.

Another crucial part of learning is confidence in our judgements. If we aren't confident enough in a decision, we'll decide that it may not be the correct one. For instance, each tiem you meet a friend, your brain is thinking "Ah, I'm 99% sure that's my friend Pat". On the flipside, I'm short sighted but silly enough to not wear my glasses. As such, I might recognise the general facial features of someone across the street but I can't see enough detail to be sure. My own brain is thinking "I'm only 40% confident and I would hesitate in calling that a correct match".

It's a bit hand wavy but in essence, those are the two important elements. A machine learns by being fed data continuously and having its output judged. A facial detection machine may be trained on photos of a single person and then asked to identify them in photos of a crowded airport. It would respond Yes or No along with its level of confidence which can be checked against the actual answer. Those results are then fed back into the machine and it continues to improve itself as time goes on.

So how does this relate to deepfakes? Well, it's a type of neural network. A what now, you say? It's essentially what I just described which is a network that takes an output, does some unknown (hidden) calculations in the middle and returns an output. There's many different networks with different amounts of inputs and outputs but for the case of deepfakes, we're only dealing with 1 input and 1 output.

According to [this](https://www.reddit.com/r/deepfakes/comments/7pgcg4/detailed_explanation_of_the_algorithm/) somewhat confusing and not user-friendly series of explainations, it centers around two autoencoders which I'll break down shortly.

For this particular case, a neural network is little more t