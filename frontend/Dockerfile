FROM node:20

WORKDIR /app

# Copy dependencies and install
COPY package*.json ./
RUN npm install

# Copy source *after* installing dependencies
COPY . .

# Build the app
RUN npm run build

# Install serve globally
RUN npm install -g serve

EXPOSE 5173

# Serve the built app
CMD ["serve", "-s", "dist", "-l", "5173"]

