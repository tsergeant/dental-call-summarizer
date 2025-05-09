FROM node:20
WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev"]

# Uncomment the following lines if you want to build the app for production
#RUN npm install && npm run build
#RUN npm install -g serve
#CMD ["serve", "-s", "dist", "-l", "5173"]
