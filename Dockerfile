# base image
FROM mcr.microsoft.com/playwright:v1.57.0-noble

# set working dir
WORKDIR /playwright-test

# copy package files into working dir ./
COPY package*.json ./

# install dependencies
RUN npm install

# copy other files
COPY . .

# run tests
CMD ["npx", "playwright", "test", "--project=apiTests"]
