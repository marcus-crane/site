# Things I Made <https://thingsima.de>

This is my personal site. There are many like it but this one is mine!

# Overview

My site is always a work in progress but currently it consists of 3 pages: Home, Blog and Stats. While the first is nothing more than a placeholder, the other two have a little bit more going on under the hood.

## Blog

The blog section of my site isn't too different from traditional Django blogs. It defines a generic Post model and uses the default Django admin because it works perfectly fine. Where it starts to divert a little is through it's use of Markdown. I specifically use [mistune](https://github.com/lepture/mistune) which claims to be the fastest Python markdown parser, not that I'm worried about speed in this case.

On a side note, mistune is not what I'd consider beginner friendly if you're new to Python. It's fine for basic Markdown but if you want to extend it to support ie blockquotes, code blocks and what not, it's not super straight forward I found. I had to learn a bit to wrap my head around it but now this project serves as an example of it running in the wild which is neat. My custom parser for blockquotes is pretty rubbish but it does the job.

## Stats

The stats section is easily my favourite and is where the bulk of work has gone. You can see it [here](https://thingsima.de/stats) where it shows recent media that I've been consuming. It's not static, it actually pulls directly from various APIs and automatically updates every so often! There's even a hidden endpoint for triggering a manual update so I can say "Alexa, trigger manual site refresh" and it'll refresh my stats. It started as a dumb idea and just kinda kept growing over time. I don't know if I consider it a "good" idea but it's something I thought of as a kid and now I've finally learnt enough to make it come true.

In order to update stats on a cycle, I use a [Celery](http://www.celeryproject.org/) worker that queues updates using [RabbitMQ](https://www.rabbitmq.com/). Honestly, it's a glorified cron scheduler and I'm thinking about converting them to AWS [Lambdas](https://aws.amazon.com/lambda/features/) that get triggered by [Cloudwatch](https://aws.amazon.com/cloudwatch). I struggled to find examples of projects that used Django AND Celery AND RabbitMQ, let alone included a Docker Compose setup so enjoy.

# Local Development

If you attempt to develop locally, you'll be bugged for a `keys.ini` file which lives in `site/thingsimade`. You can see an example template inside `site/thingsimade/ex_keys.ini`. They're not all needed or even used, I just haven't cleaned up the file is all. You can just fill them with garbage (or rename `ex_keys.ini` to `keys.ini`) and ignore any errors that pop up. They're only used by Celery anyway so it should be fine. You'll just have an empty database when you try to render the stats page is all.

The quickest way to get set up is using Docker. If you've got it installed, running `make dev` should get you setup.

# Deployment

I don't know why you'd want to deploy my site because, well, it's mine but I just deploy it as a background Docker process and then point it to an nginx config on a [Vultr](https://www.vultr.com/) VPS.

As mentioned before, I'm looking at breaking this setup into smaller bits and deploying it on AWS for fun and learning. If I do get around to that, I'll likely archive this repository for historical/reference purposes.

Thanks for reading!