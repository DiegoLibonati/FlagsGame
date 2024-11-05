FROM node:19

WORKDIR /home/app

COPY package*.json ./

RUN yarn install --ignore-engines

COPY . .

EXPOSE 3000

CMD ["yarn", "start"]
