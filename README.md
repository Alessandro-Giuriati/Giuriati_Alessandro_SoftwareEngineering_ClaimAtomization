# Claim Atomization

## Project Overview
This project is developed for the Software Engineering module as an individual toy project.

The goal of the system is to process a single news article and transform it into an ordered list of atomic factual claims. The granularity of the output is not fixed in advance, but should reflect how much factual information the article actually contains.

## Current Scope
At the current stage, the system is intentionally limited to:
- one article at a time;
- locally stored text files as input;
- ordered output in the form of atomic factual claims.

## Planned Features
The first implementation iteration will focus on:
- loading a single local text article;
- validating the input;
- preparing the article text for processing;
- generating atomic claims;
- returning the claims in an ordered and readable format.