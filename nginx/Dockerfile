FROM nginx:latest
COPY ./nginx.conf /etc/nginx/nginx.conf


FROM nginx:latest


# Copy your custom Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]

