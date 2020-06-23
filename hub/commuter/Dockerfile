# Credit: https://github.com/nteract/commuter/blob/master/Dockerfile
# License: BSD-3-Clause License
##################################
# Build
##################################
FROM node:14 as build

RUN mkdir -p /opt/build

WORKDIR /opt/build

COPY ./src ./src
COPY [ \
  "babel.config.js", \
  "next.config.js", \
  "package.json", \
  "yarn.lock", \
  "./" \
]

RUN yarn install && \
  yarn build

##################################
# Dependencies
##################################
FROM node:14 as dependencies

RUN DEBIAN_FRONTEND=noninteractive \
  apt-get update && \
  apt-get install --yes --no-install-recommends \
  build-essential \
  libcairo2-dev \
  libpango1.0-dev \
  libjpeg-dev \
  libgif-dev \
  librsvg2-dev && \
  \
  rm -rf /var/lib/apt/lists/*

ENV NODE_ENV='production'

RUN mkdir -p /opt/build

WORKDIR /opt/build

COPY --from=build [ \
  "/opt/build/package.json", \
  "/opt/build/yarn.lock", \
  "./" \
]

RUN yarn install --production=true

##################################
# Release
##################################
FROM node:14-slim as release

# Install tini
ARG TINI_VERSION=v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

ENV NODE_ENV='production'

RUN mkdir -p /opt/app

WORKDIR /opt/app

COPY --from=build /opt/build/.next /opt/app/.next
COPY --from=build /opt/build/lib /opt/app/lib
COPY --from=build /opt/build/public /opt/app/public
COPY --from=dependencies /opt/build/node_modules /opt/app/node_modules

ENTRYPOINT ["/tini", "-g", "--"]
CMD [ "node", "lib/index.js" ]
