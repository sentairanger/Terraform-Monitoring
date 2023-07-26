from flask import Flask, request, render_template
from gpiozero import OutputDevice, LED, PWMOutputDevice, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from prometheus_flask_exporter import PrometheusMetrics

factory = PiGPIOFactory(host='192.168.0.28')
factory2 = PiGPIOFactory(host='192.168.0.10')

led = LED(25, pin_factory=factory)
en_1 = PWMOutputDevice(12, pin_factory=factory)
en_2 = PWMOutputDevice(26, pin_factory=factory)
motor_in1 = OutputDevice(13, pin_factory=factory)
motor_in2 = OutputDevice(21, pin_factory=factory)
motor_in3 = OutputDevice(17, pin_factory=factory)
motor_in4 = OutputDevice(27, pin_factory=factory)
angular_servo = AngularServo(22, min_angle=-90, max_angle=90, pin_factory=factory)
angular_servo2 = AngularServo(23, min_angle=-90, max_angle=90, pin_factory=factory)

eye = LED(25, pin_factory=factory2)
en_3 = PWMOutputDevice(12, pin_factory=factory2)
en_4 = PWMOutputDevice(26, pin_factory=factory2)
pin1 = OutputDevice(13, pin_factory=factory2)
pin2 = OutputDevice(21, pin_factory=factory2)
pin3 = OutputDevice(17, pin_factory=factory2)
pin4 = OutputDevice(27, pin_factory=factory2)


app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)

# Apply the same metric to all of the endpoints
endpoint_counter = metrics.counter(
    'endpoint_counter', 'Request count by endpoints',
    labels={'endpoint': lambda: request.endpoint}
)


@app.route("/")
@endpoint_counter
def hello():
    return render_template("index.html")

@app.route("/forward")
@endpoint_counter
def forward():
    motor_in1.on()
    motor_in2.off()
    motor_in3.on()
    motor_in4.off()
    return render_template("index.html")

@app.route("/backward")
@endpoint_counter
def backward():
    motor_in1.off()
    motor_in2.on()
    motor_in3.off()
    motor_in4.on()
    return render_template("index.html")

@app.route("/left")
@endpoint_counter
def left():
    motor_in1.off()
    motor_in2.on()
    motor_in3.on()
    motor_in4.off()
    return render_template("index.html")

@app.route("/right")
@endpoint_counter
def right():
    motor_in1.on()
    motor_in2.off()
    motor_in3.off()
    motor_in4.on()
    return render_template("index.html")

@app.route("/stop")
@endpoint_counter
def stop():
    motor_in1.off()
    motor_in2.off()
    motor_in3.off()
    motor_in4.off()
    return render_template("index.html")

@app.route("/north")
@endpoint_counter
def north():
    pin1.on()
    pin2.off()
    pin3.on()
    pin4.off()
    return render_template("index.html")

@app.route("/south")
@endpoint_counter
def south():
    pin1.off()
    pin2.on()
    pin3.off()
    pin4.on()
    return render_template("index.html")

@app.route("/west")
@endpoint_counter
def west():
    pin1.off()
    pin2.on()
    pin3.on()
    pin4.off()
    return render_template("index.html")

@app.route("/east")
@endpoint_counter
def east():
    pin1.on()
    pin2.off()
    pin3.off()
    pin4.on()
    return render_template("index.html")

@app.route("/stop2")
@endpoint_counter
def stop2():
    pin1.off()
    pin2.off()
    pin3.off()
    pin4.off()
    return render_template("index.html")

@app.route("/on")
@endpoint_counter
def on():
    led.on()
    return render_template("index.html")

@app.route("/off")
@endpoint_counter
def off():
    led.off()
    return render_template("index.html")

@app.route("/eyeon")
@endpoint_counter
def eyeon():
    eye.on()
    return render_template("index.html")

@app.route("/eyeoff")
@endpoint_counter
def eyeoff():
    eye.off()
    return render_template("index.html")


@app.route('/motorpwm', methods=['POST'])
@endpoint_counter
def motorpwm():
    slider = request.form["speed"]
    en_1.value = int(slider) / 10
    en_2.value = int(slider) / 10
    en_3.value = int(slider) / 10
    en_4.value = int(slider) / 10
    return render_template('index.html')
    

@app.route('/servoarm', methods=['POST'])
@endpoint_counter
def servoarm():
    slider1 = request.form["degree"]
    slider2 = request.form["degree2"]
    angular_servo.angle = int(slider1)
    angular_servo2.angle = int(slider2)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
