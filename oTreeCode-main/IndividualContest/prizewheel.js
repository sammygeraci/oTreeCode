class Sector {
  constructor(color, angle) {
    this.color = color;
    this.angle = angle;
  }
}

class PrizeWheel {
  constructor(options) {
    options = options || {};
    const defaults = {
      initialSpeed: 8 * Math.PI,
      friction: 0.6,
      minSpeed: 0.001
    }
    let settings = Object.assign({}, defaults, options);
    if (settings.canvasId) {
      this.canvas = document.getElementById(settings.canvasId);
    }
    else {
      this.canvas = document.createElement('canvas');
    }
    this.ctx = this.canvas.getContext('2d');
    if (!settings.sectors) {
      const colors = [
        '#f73434', '#f78834', '#faf02d', '#18ba2b', '#235fd9', '#6d24d4', '#c224d4'
      ];
      const angle = 2 * Math.PI / colors.length;
      this.sectors = [];
      for (const color of colors) {
        this.sectors.push(new Sector(color, angle));
      }
    }
    else {
      this.sectors = settings.sectors;
    }
    this.needleAngle = 0;
    this.initialSpeed = settings.initialSpeed;
    this.friction = settings.friction;
    this.target = null;
    this.TWO_PI = 2 * Math.PI;
    this.minSpeed = settings.minSpeed;
    this.isDecelerating = false;
    this.isMoving = false;
    this.startTime = null;
    this.prizeCallback = settings.prizeCallback;
    window.requestAnimationFrame(this.update.bind(this));
  }

  spin(target) {
    this.target = target;
    this.speedOverLog = this.initialSpeed / Math.log(1 - this.friction);
    this.threshold = (
      this.TWO_PI + (this.target + this.speedOverLog) % this.TWO_PI
    ) % this.TWO_PI;
    this.isMoving = true;
    this.isDecelerating = false;
    this.startTime = null;
  }

  drawWheel() {
    this.ctx.save();

    this.ctx.translate(
      0.5 * this.canvas.width, 0.5 * this.canvas.height
    );
    this.ctx.rotate(-0.5 * Math.PI);

    for (let i = 0; i < this.sectors.length; i++) {
      const sector = this.sectors[i];
      this.ctx.fillStyle = sector.color;
      this.ctx.beginPath();
      this.ctx.moveTo(0, 0);
      const overlap = 0.03;
      let angleA = 0;
      let angleB = sector.angle;
      if (!i) angleA -= overlap;
      if (i !== this.sectors.length - 1) angleB += overlap;
      this.ctx.arc(0, 0, 0.5 * this.canvas.width, angleA, angleB);
      this.ctx.fill();

      this.ctx.rotate(sector.angle);
    }

    this.ctx.strokeStyle = '#000';
    this.ctx.lineWidth = 2;
    this.ctx.beginPath();
    this.ctx.arc(0, 0, 0.5 * this.canvas.width - 1, 0, this.TWO_PI);
    this.ctx.stroke();

    this.ctx.restore();
  }

  drawNeedle() {
    const halfWidth1 = 4;
    const halfWidth2 = 1;
    const length = 0.45 * this.canvas.width;

    this.ctx.save();

    this.ctx.translate(
      0.5 * this.canvas.width, 0.5 * this.canvas.height
    );
    this.ctx.rotate(this.needleAngle - 0.5 * Math.PI);

    this.ctx.fillStyle = '#000';

    this.ctx.beginPath();
    this.ctx.moveTo(0, -halfWidth1);
    this.ctx.lineTo(length, -halfWidth2);
    this.ctx.lineTo(length, halfWidth2);
    this.ctx.lineTo(0, halfWidth1);
    this.ctx.fill();

    this.ctx.beginPath();
    this.ctx.arc(0, 0, halfWidth1, 0, this.TWO_PI);
    this.ctx.fill();

    this.ctx.restore();
  }

  updateNeedleAngle(timestamp) {
    if (!this.isMoving) return;
    if (!this.startTime) this.startTime = timestamp;
    if (!this.isDecelerating && this.needleAngle >= this.threshold) {
      this.isDecelerating = true;
      this.startTime = timestamp;
      this.needleAngle = this.threshold;
    }
    else {
      const seconds = (timestamp - this.startTime) * 0.001;
      if (this.isDecelerating) {
        const coefficient = (1 - this.friction) ** seconds;
        const speed = this.initialSpeed * coefficient;
        if (speed < this.minSpeed) {
          this.needleAngle = this.target;
          this.isMoving = false;
          this.isDecelerating = false;
          const prize = this.getPrize();
          if (this.prizeCallback) this.prizeCallback(prize);
        }
        else {
          this.needleAngle = this.target + this.speedOverLog * coefficient;
        }
      }
      else {
        this.needleAngle = this.initialSpeed * seconds;
      }
    }
  }

  getPrize() {
    const needleAngle = (
      this.TWO_PI + this.needleAngle % this.TWO_PI
    ) % this.TWO_PI;
    let prizeAngle = 0;
    for (let i = 0; i < this.sectors.length; i++) {
      prizeAngle += this.sectors[i].angle;
      if (prizeAngle > needleAngle) return i;
      if (prizeAngle === needleAngle) {
        let x = Math.random();
        if (x < 0.5) return i;
      }
    }
  }

  update(timestamp) {
    this.updateNeedleAngle(timestamp);
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.drawWheel();
    this.drawNeedle();
    window.requestAnimationFrame(this.update.bind(this));
  }
}