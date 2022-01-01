from ubuntu:20.04

ENV pubkey="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCr+005M4XRhQrK91crAWSFucwId8b3vnBCmIGiiU+7s0whjs3SJHNxle/Z6c++kvY8Os6MGiBHIOCj3ORZY1QZRLUk5olK8zvI5M5K/roIM32X1YVk92DgKteDDlYzYLWc7pp3KL+zFEvZs7uTQAR2uxoR9CtmRd4zwLjgy+NSstf8gvVni2OW1qXsUNulCeimBwK7TIWzk/AKsKs4UiGLFAV5uyn/IuUl9pdEgcNPzZIL855+2XALU8O/Y5TC0NA5/MjxKBITwE7X+M8oDDH8xAPh9BnNwTHlbxxZJgupBd3EuGCIWXDd/ogxbEOVnmszlTzjkt2MNw/no/p8k8L3zPVwkHPezi3oeNlA6vPJMzmu0kTm7SO4r97J+Kwt1oA9BJ4xsWtRZ0UmLZSLjYtT3GLx2M8IQOMUg1JgWaRUSdEFvqZppZcNMk9Utx0r804VO7pY6N2KaJqbxDLUGTrHxTB7bQqA7hXDxUFiNbl43s5nXgeNCn2xsszW4KFmob8= lnrcdr@lnrcdr-B360M-D3H"
ENV sshport=2222
WORKDIR /api
COPY ./api ./

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ADD https://github.com/just-containers/s6-overlay/releases/download/v2.2.0.1/s6-overlay-amd64-installer /tmp/
RUN chmod +x /tmp/s6-overlay-amd64-installer && /tmp/s6-overlay-amd64-installer /
RUN chmod +x install.sh && sed -i -e 's/\r$//' install.sh && ./install.sh
RUN ssh-keygen -t rsa -f ~/.ssh/id_rsa -N ""
ADD api/services.d/ssh /root/ssh.sh
RUN chmod 755 /root/ssh.sh && sed -i -e 's/\r$//' /root/ssh.sh

ENTRYPOINT ["/root/ssh.sh"]