# 📧 Mail Service - Guide d'utilisation

Service d'envoi d'emails prêt à l'emploi via API REST. Intégrez facilement l'envoi d'emails dans vos projets sans réécrire le code SMTP.

## 🚀 Démarrage rapide

### Utilisation avec Docker Hub

```bash
# Récupérer l'image depuis Docker Hub
docker pull kalagaserge/mail_service

# Lancer le conteneur avec les variables d'environnement
docker run -d \
  --name mail_service \
  -p 9876:9876 \
  -e EMAIL_DOMAIN=votre-domaine.com \
  -e EMAIL_HOST=smtp.votre-fournisseur.com \
  -e EMAIL_PORT=587 \
  -e EMAIL_USERNAME=votre-email@domaine.com \
  -e EMAIL_PASSWORD=votre-mot-de-passe \
  -e FROM_EMAIL=noreply@votre-domaine.com \
  kalagaserge/mail_service
```

### Utilisation avec Docker Compose

Créez un fichier `docker-compose.yml` :

```yaml
version: '3.8'

services:
  mail_service:
    image: kalagaserge/mail_service
    container_name: mail_service
    ports:
      - "9876:9876"
    environment:
      - EMAIL_DOMAIN=votre-domaine.com
      - EMAIL_HOST=smtp.votre-fournisseur.com
      - EMAIL_PORT=587
      - EMAIL_USERNAME=votre-email@domaine.com
      - EMAIL_PASSWORD=votre-mot-de-passe
      - FROM_EMAIL=noreply@votre-domaine.com
    restart: unless-stopped
```

Puis lancez le service :

```bash
docker-compose up -d
```

## ⚙️ Configuration

### Variables d'environnement obligatoires

| Variable | Description | Exemple |
|----------|-------------|---------|
| `EMAIL_DOMAIN` | Domaine de votre organisation | `monentreprise.com` |
| `EMAIL_HOST` | Serveur SMTP | `smtp.gmail.com` |
| `EMAIL_PORT` | Port SMTP (généralement 587) | `587` |
| `EMAIL_USERNAME` | Nom d'utilisateur SMTP | `admin@monentreprise.com` |
| `EMAIL_PASSWORD` | Mot de passe SMTP | `motdepasse123` |

### Variables d'environnement optionnelles

| Variable | Description | Défaut |
|----------|-------------|--------|
| `FROM_EMAIL` | Adresse email d'expéditeur | `noreply@{EMAIL_DOMAIN}` |

### Configuration par fournisseur

#### Gmail
```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=votre-email@gmail.com
EMAIL_PASSWORD=mot-de-passe-application
```

#### Outlook/Hotmail
```bash
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USERNAME=votre-email@outlook.com
EMAIL_PASSWORD=votre-mot-de-passe
```

#### Mailgun
```bash
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_USERNAME=postmaster@votre-domaine.mailgun.org
EMAIL_PASSWORD=votre-clé-api
```

## 📝 API Documentation

Une fois le service démarré, l'API est accessible sur `http://localhost:9876`

### Documentation interactive

- **Swagger UI** : `http://localhost:9876/docs`
- **ReDoc** : `http://localhost:9876/redoc`

### Endpoints disponibles

#### GET `/`
Endpoint de vérification du service

**Réponse :**
```json
{
  "message": "Welcome to the Mail Service API"
}
```

#### POST `/api/send-email`
Envoi d'un email

**Corps de la requête :**
```json
{
  "receiver_email": "destinataire@exemple.com",
  "email_object": "Sujet de l'email",
  "message_text": "Contenu de l'email"
}
```

**Paramètres :**

- `receiver_email` (obligatoire) : Adresse email du destinataire ou liste d'adresses
- `email_object` (optionnel) : Sujet de l'email (défaut : "No Subject")
- `message_text` (obligatoire) : Contenu de l'email (supporte HTML)

**Réponse en cas de succès :**
```json
{
  "message": "Email sent successfully"
}
```

#### GET `/api/smtp-status`
Vérification du statut du serveur SMTP

**Réponse :**
```json
{
  "status": true,
  "message": "SMTP server is reachable."
}
```

**États possibles :**
- `status: true` : Le serveur SMTP est accessible et les identifiants sont valides
- `status: false` : Le serveur SMTP n'est pas accessible ou les identifiants sont incorrects

## 💡 Exemples d'utilisation

### Envoi d'un email simple

```bash
curl -X POST "http://localhost:9876/api/send-email" \
  -H "Content-Type: application/json" \
  -d '{
    "receiver_email": "user@example.com",
    "email_object": "Test Email",
    "message_text": "Bonjour, ceci est un email de test."
  }'
```

### Envoi à plusieurs destinataires

```bash
curl -X POST "http://localhost:9876/api/send-email" \
  -H "Content-Type: application/json" \
  -d '{
    "receiver_email": [
      "user1@example.com", 
      "user2@example.com", 
      "user3@example.com"
    ],
    "email_object": "Newsletter hebdomadaire",
    "message_text": "<h1>Newsletter</h1><p>Contenu de la newsletter...</p>"
  }'
```

### Envoi d'email HTML

```bash
curl -X POST "http://localhost:9876/api/send-email" \
  -H "Content-Type: application/json" \
  -d '{
    "receiver_email": "client@example.com",
    "email_object": "Bienvenue !",
    "message_text": "<html><body><h2>Bienvenue dans notre service !</h2><p>Merci de vous être inscrit.</p><a href=\"https://monsite.com\">Visitez notre site</a></body></html>"
  }'
```

### Intégration Python

```python
import requests
import json

def send_email(to_email, subject, content):
    url = "http://localhost:9876/api/send-email"
    payload = {
        "receiver_email": to_email,
        "email_object": subject,
        "message_text": content
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("Email envoyé avec succès !")
        return True
    else:
        print(f"Erreur lors de l'envoi : {response.text}")
        return False

# Utilisation
send_email(
    to_email="client@example.com",
    subject="Confirmation de commande",
    content="<h2>Votre commande est confirmée</h2><p>Numéro : #12345</p>"
)
```

### Intégration JavaScript/Node.js

```javascript
const axios = require('axios');

async function sendEmail(toEmail, subject, content) {
    try {
        const response = await axios.post('http://localhost:9876/api/send-email', {
            receiver_email: toEmail,
            email_object: subject,
            message_text: content
        });
        
        console.log('Email envoyé avec succès !');
        return response.data;
    } catch (error) {
        console.error('Erreur lors de l\'envoi :', error.response.data);
        throw error;
    }
}

// Utilisation
sendEmail(
    'client@example.com',
    'Notification importante',
    '<p>Votre compte a été mis à jour.</p>'
);
```

### Vérification du statut SMTP

```bash
# Vérifier si le serveur SMTP est accessible
curl http://localhost:9876/api/smtp-status
```

**Réponse en cas de succès :**
```json
{
  "status": true,
  "message": "SMTP server is reachable."
}
```

**Réponse en cas d'erreur :**
```json
{
  "status": false,
  "message": "SMTP server is not reachable."
}
```


## 🔧 Gestion des erreurs

### Codes de statut HTTP

- `200` : Email envoyé avec succès
- `400` : Données invalides (adresse email incorrecte, configuration manquante)
- `500` : Erreur serveur (problème SMTP, configuration incorrecte)

### Messages d'erreur courants

```json
{
  "detail": "Invalid email address"
}
```

```json
{
  "detail": "Email configurations are not properly set."
}
```

```json
{
  "detail": "Error sending email: [détails de l'erreur SMTP]"
}
```

## 📊 Diagnostic et monitoring

### Vérification de l'état du service

```bash
# Vérifier que le service répond
curl http://localhost:9876/

# Vérifier la documentation API
curl http://localhost:9876/docs

# Tester la connectivité SMTP
curl http://localhost:9876/api/smtp-status
```

```bash
# Test d'envoi d'email (optionnel)
echo "3. Test d'envoi d'email de diagnostic..."
curl -X POST "http://localhost:9876/api/send-email" \
  -H "Content-Type: application/json" \
  -d '{
    "receiver_email": "admin@votre-domaine.com",
    "email_object": "Test de diagnostic - Mail Service",
    "message_text": "Ce message confirme que le service fonctionne correctement."
  }'

echo "=== Fin du diagnostic ==="
```

## 🔁 Intégration Kafka

Le service peut consommer des messages Kafka pour envoyer automatiquement des emails si l'intégration Kafka est activée via les variables d'environnement (`USE_KAFKA`, `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_CONSUMER_TOPIC`, `KAFKA_MESSAGE_KEY`).

Format JSON attendu pour le message (payload) avec la clé Kafka `email_topic` (vous pouvez modifier la clé via `KAFKA_MESSAGE_KEY`) :

```json
{
  "receiver_email": "user@example.com",
  "email_object": "Sujet",
  "message_text": "Contenu du message"
}
```

Points importants pour une intégration en production ou en environnement conteneurisé :

- Le conteneur qui exécute le service doit être sur le même réseau Docker que le broker Kafka afin d'utiliser l'adresse interne du broker (ex. `broker:9093`). Sans réseau partagé, la résolution de nom et la connexion échoueront.
- Pour les clients externes (depuis la machine hôte), utilisez l'endpoint exposé du broker (ex. `localhost:9092`) si les ports sont mappés.
- Assurez-vous que `KAFKA_BOOTSTRAP_SERVERS` pointe vers l'endpoint correct selon le contexte (interne au réseau Docker vs externe).
- Vérifiez que le topic configuré (`KAFKA_CONSUMER_TOPIC`) correspond au topic sur lequel sont publiés les messages.

Exemple minimal (attacher le service au réseau Docker interne du broker) :
```yaml
version: '3.8'

networks:
  local-kafka:
    external: true

services:
  mail_service:
    image: kalagaserge/mail_service
    container_name: mail_service
    ports:
      - "9876:9876"
    environment:
      - USE_KAFKA=True
      - KAFKA_BOOTSTRAP_SERVERS=broker:9093
      - KAFKA_CONSUMER_TOPIC=email_topic
      - KAFKA_MESSAGE_KEY=email_topic
    networks:
      - local-kafka
    restart: unless-stopped
```

## 🐰 Intégration RabbitMQ

Le service peut consommer des messages RabbitMQ pour envoyer automatiquement des emails si l'intégration RabbitMQ est activée via les variables d'environnement (`USE_RABBITMQ`, `RABBITMQ_URL`, `RABBITMQ_EXCHANGE`, `RABBITMQ_ROUTING_KEY`, `RABBITMQ_QUEUE`).

Format JSON attendu pour le message publié sur RabbitMQ :

```json
{
  "receiver_email": "user@example.com",
  "email_object": "Sujet",
  "message_text": "Contenu du message"
}
```

### Variables d'environnement RabbitMQ

| Variable | Description | Exemple |
|----------|-------------|---------|
| `USE_RABBITMQ` | Activer l'intégration RabbitMQ | `True` |
| `RABBITMQ_URL` | URL de connexion RabbitMQ | `amqp://admin:admin@rabbitmq:5672` |
| `RABBITMQ_EXCHANGE` | Nom de l'exchange | `email_exchange` |
| `RABBITMQ_ROUTING_KEY` | Routing key pour lier la queue | `email_routing_key` |
| `RABBITMQ_QUEUE` | Nom de la queue | `email_queue` |
| `RABBITMQ_DEFAULT_USER` | Utilisateur RabbitMQ | `admin` |
| `RABBITMQ_DEFAULT_PASS` | Mot de passe RabbitMQ | `admin` |

### Points importants pour l'intégration RabbitMQ

- Le conteneur qui exécute le service doit être sur le même réseau Docker que RabbitMQ afin d'utiliser l'adresse interne (ex. `rabbitmq:5672`). Sans réseau partagé, la résolution de nom et la connexion échoueront.
- Pour les clients externes (depuis la machine hôte), utilisez l'endpoint exposé de RabbitMQ (ex. `localhost:5672`) si les ports sont mappés.
- Assurez-vous que `RABBITMQ_URL` pointe vers l'endpoint correct selon le contexte (interne au réseau Docker vs externe).
- Vérifiez que l'exchange et la routing key configurés correspondent à ceux utilisés par vos producteurs de messages.
- Le service déclare automatiquement l'exchange de type `TOPIC` et la queue durable, puis les lie avec la routing key spécifiée.


## 🚨 Sécurité et bonnes pratiques

### Recommandations de sécurité

1. **Utilisez des mots de passe d'application** pour Gmail (pas votre mot de passe principal)
2. **Limitez l'accès** au port 9876 dans votre pare-feu
3. **Utilisez HTTPS** en production avec un reverse proxy (nginx, traefik)
4. **Stockez les secrets** de manière sécurisée (Docker secrets, variables d'environnement chiffrées)
5. **Surveillez régulièrement** le statut SMTP avec l'endpoint `/api/smtp-status`


---


**Développé avec ❤️ par Kalaga Serge**

<!-- Mes coordonnées Github -->

- [Projet GitHub](https://github.com/serge-eric-kalaga/MailService)
- [Profil GitHub - serge-eric-kalaga](https://github.com/serge-eric-kalaga)
