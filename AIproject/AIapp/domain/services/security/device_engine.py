import hashlib

from AIapp.models import DeviceFingerprint


class DeviceEngine:

    NEW_DEVICE_RISK = 40
    NEW_IP_RISK = 30
    SUSPICIOUS_AGENT_RISK = 20

    def evaluate(self, user, request):

        # Celery tasks do not have HTTP request
        if request is None:
            return 0

        ip = self._get_ip(request)

        user_agent = request.META.get("HTTP_USER_AGENT", "")

        device_hash = self._generate_device_hash(ip, user_agent)

        risk_score = 0

        # Проверка нового устройства
        device_exists = DeviceFingerprint.objects.filter(
            user=user,
            device_hash=device_hash
        ).exists()

        if not device_exists:
            risk_score += self.NEW_DEVICE_RISK

        # Проверка нового IP
        ip_exists = DeviceFingerprint.objects.filter(
            user=user,
            ip_address=ip
        ).exists()

        if not ip_exists:
            risk_score += self.NEW_IP_RISK

        # Проверка подозрительного user-agent
        if self._is_suspicious_agent(user_agent):
            risk_score += self.SUSPICIOUS_AGENT_RISK

        # Сохраняем fingerprint если устройство новое
        if not device_exists:
            DeviceFingerprint.objects.create(
                user=user,
                ip_address=ip,
                user_agent=user_agent,
                device_hash=device_hash
            )

        return risk_score

    def _generate_device_hash(self, ip, user_agent):

        raw = f"{ip}-{user_agent}"

        return hashlib.sha256(raw.encode()).hexdigest()

    def _get_ip(self, request):

        if request is None:
            return None

        x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded:
            return x_forwarded.split(",")[0]

        return request.META.get("REMOTE_ADDR")

    def _is_suspicious_agent(self, user_agent):

        suspicious_keywords = [
            "python",
            "curl",
            "bot",
            "scraper",
            "postman",
        ]

        ua = user_agent.lower()

        return any(keyword in ua for keyword in suspicious_keywords)