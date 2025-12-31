# ClubHub - Quick Start Guide

## 🚀 Run with Docker (Recommended)

### Start the application:
```bash
docker compose up --build
```

### Access the application:
- **Website**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/

### Default credentials:
- **Username**: `admin`
- **Password**: `admin123`

### Stop the application:
Press `Ctrl+C` in the terminal, then:
```bash
docker compose down
```

---

## 📋 What You Get

✅ **Fully functional Django app** with PostgreSQL database  
✅ **Auto-created admin user** (username: admin, password: admin123)  
✅ **All migrations applied** automatically  
✅ **Static files collected** and ready  
✅ **Hot reload enabled** - code changes reflect immediately  

---

## 🔧 Common Commands

### View logs:
```bash
docker compose logs -f
```

### Run Django commands:
```bash
docker compose exec web python3 manage.py <command>
```

Examples:
```bash
# Create a new admin user
docker compose exec web python3 manage.py createsuperuser

# Run tests
docker compose exec web python3 manage.py test

# Open Django shell
docker compose exec web python3 manage.py shell
```

### Reset everything (fresh start):
```bash
docker compose down -v
docker compose up --build
```

---

## 📚 Features Implemented

### ✅ Core Features
- User authentication (signup, login, logout)
- Club creation and management
- Club discovery with search/filter
- Membership request system
- Role-based permissions (Admin, Moderator, Member)
- Post creation (Blog & News posts)
- Member promotion/demotion

### ✅ Role Permissions
- **Admin**: Approve/reject requests, promote members, create all post types
- **Moderator**: Create Blog & News posts
- **Member**: Create Blog posts only

### ✅ Guest Users
- Browse clubs
- View club details and posts
- Must login to join clubs

---

## 🌐 Ports

- **8000** - Django web application
- **5433** - PostgreSQL database (mapped from container's 5432)

---

## 📖 Documentation

- **[DOCKER_SETUP.md](./DOCKER_SETUP.md)** - Complete Docker documentation
- **[README.md](./README.md)** - Project requirements and specifications
- **[CLAUDE.md](./CLAUDE.md)** - Development guidelines and architecture

---

## 🐛 Troubleshooting

### Port already in use?
Change the port in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Changed from 8000 to 8001
```

### Database connection issues?
```bash
docker compose down -v
docker compose up --build
```

### Permission errors?
```bash
chmod +x docker-entrypoint.sh
docker compose down
docker compose up --build
```

---

## 💡 Tips

1. **Code changes** are immediately reflected (hot reload enabled)
2. **Database data** persists between restarts (stored in Docker volume)
3. **Static files** are automatically collected on startup
4. **Superuser** is created automatically if credentials are in `.env`

---

## 🎯 Next Steps

1. Start the application: `docker compose up --build`
2. Visit http://localhost:8000
3. Create some test clubs
4. Test the membership workflow
5. Try different user roles

---

## ⚠️ Production Notes

For production deployment:
- Change `SECRET_KEY` in `.env`
- Set `DEBUG=False`
- Update `ALLOWED_HOSTS`
- Use strong passwords
- Configure HTTPS/SSL
- Use Gunicorn instead of runserver

See [DOCKER_SETUP.md](./DOCKER_SETUP.md) for production setup details.
