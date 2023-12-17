FROM node:21.4-bookworm

COPY . /app/frontend/

WORKDIR /app/frontend

RUN npm install

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
