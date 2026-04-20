# Этап 1: Сборка (Меняем 18 на 20)
FROM node:20-alpine AS build-stage
WORKDIR /app

# Сначала копируем только файлы зависимостей для кэширования слоев
COPY package*.json ./
RUN npm install

# Копируем остальной код
COPY . .

# Теперь билд пройдет успешно
RUN npm run build

# Этап 2: Раздача через Nginx
FROM nginx:stable-alpine AS production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]