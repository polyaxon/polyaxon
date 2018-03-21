# How to contribute

Polyaxon project would love to welcome your contributions. There are several ways to help out:

* Create an [issue](https://github.com/polyaxon/polyaxon/issues) on GitHub, if you have found a bug
* Write test cases for open bug issues
* Write patches for open bug/feature issues, preferably with test cases included
* Contribute to the documentation
* Blog about different ways you are using Polyaxon

There are a few guidelines that we need contributors to follow so that we have a chance of keeping on top of things.

## Reporting issues

Polyaxon has probably many issues and bugs, a great way to contribute to the project is to send a detailed report when you encounter an issue. We always appreciate a well-written, thorough bug report, and will thank you for it!

Sometimes  Polyaxon is missing a feature you need, and we encourage our users to create and contribute such features.

Check the current [issues](https://github.com/polyaxon/polyaxon/issues) if doesn't already include that problem or suggestion before submitting an issue.
If you find a match, add a quick "+1", Doing this helps prioritize the most common problems and requests.

When reporting issues, please include your host OS (Ubuntu 14.04, CentOS 7, etc), and the version of the libraries you are using.

Please also include the steps required to reproduce the problem if possible and applicable. This information will help us review and fix your issue faster.

## Contributing

Before you contribute to Polyaxon, there are a few things that you'll need to do

* Make sure you have a [GitHub account](https://github.com/signup/free).
* Submit an [issue](https://github.com/polyaxon/polyaxon/issues), assuming one does not already exist.
  * Clearly describe the issue including steps to reproduce when it is a bug.
  * Make sure you fill in the earliest version that you know has the issue.
* Fork the repository on GitHub.

### Making Changes

* Create a topic branch from where you want to base your work.
  * This is usually the master branch.
  * Only target an existing branch if you are certain your fix must be on that branch.
  * To quickly create a topic branch based on master; `git checkout -b my_contribution origin/master`.
    It is best to avoid working directly on the `master` branch. Doing so will help avoid conflicts if you pull in updates from origin.
* Make commits of logical units. Implementing a new function and calling it in
  another file constitute a single logical unit of work.
  * A majority of submissions should have a single commit, so if in doubt, squash your commits down to one commit.
* Use descriptive commit messages and reference the #issue number.
* Core test cases should continue to pass. (Test are in progress)
* Pull requests must be cleanly rebased on top of master without multiple branches mixed into the PR.

### Which branch to base the work

All changes should be be based on the latest master commit.

## Questions

If you need help with how to use this library, please check the list of examples, if it is still unclear you can also open an issue.
