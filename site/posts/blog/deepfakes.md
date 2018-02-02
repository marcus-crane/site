Title: deepfakes
Date: January 30, 2017

First off, a disclaimer that the following post talks about a technology/community tightly tied to pornography so if you're at work, or intend to visit anything I've linked below, you do so at your own risk :)

Just under a week ago, [an article](https://www.theverge.com/2018/1/24/16929148/fake-celebrity-porn-ai-deepfake-face-swapping-artificial-intelligence-reddit) from The Verge about "fake celebrity porn" was posted on [Hacker News](https://news.ycombinator.com/item?id=16226495). If you'd just glimpsed the headline, you would assume it's a bunch of shitstirrers up to no good with Photoshop, which isn't exactly a new development but it's quite a bit worse.

I don't even write blog posts often but this thing has been kinda eating away at me that I can't not write something about it. A number of interesting, and terrifying points, were raised in the discussions that followed (HN + Verge comments) and I'll be mainly merging those with my own views to hopefully round them up into one sorta cohesive post.

**The short version**

For starters, it's worth explaining what the heck this deepfakes thing actually is. The short version is that it's using machine learning to "swap" the face of one person onto the face of another. The /r/deepfakes subreddit focuses on swapping celebrity faces with those of porn stars to create the "fake celebrity porn" mentioned before.

**The long version (those familiar with ML can skip this)**

Here's a quick rundown on how this stuff works. To quote [not Albert Einstein](https://quoteinvestigator.com/2011/05/13/einstein-simple/), "Everything should be made as simple as possible, but not simpler." and that's what I'm aiming for because I sure as heck am no expert. My coworker (at a non-tech company) seemed to understand it though so I'll just be repeating it here.

Alrighty, so there's this concept called Machine Learning. Your first thought might be "Oh, you mean AI?" but without going into [semantics](https://en.wikipedia.org/wiki/AI_effect), just note that none of these so called "AI" are actually self aware or conscious. They are just taking in data and spitting out data, whether it be as a file (a video file in this case), text to speech or some other medium.

So how does a machine "learn"? 