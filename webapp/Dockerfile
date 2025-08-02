FROM oven/bun:1

# Install OpenSSL for Prisma
RUN apt-get update -y && apt-get install -y openssl

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY bun.lockb ./

# Install dependencies
RUN bun install

# Copy Prisma schema
COPY prisma ./prisma/

# Generate Prisma client
RUN bunx prisma generate

# Copy source code
COPY . .

# Build the application (skip env validation)
ENV SKIP_ENV_VALIDATION=true
RUN bun run build

# Expose port
EXPOSE 3000

# Start the application
CMD ["bun", "start"] 