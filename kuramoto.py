from manim import *

import numpy as np

class KuramotoOscillators(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        # Number of oscillators
        N = 20
        
        # Initialize random natural frequencies
        natural_frequencies = np.random.uniform(0.8, 1.5, N)
        
        # Initialize random phases
        phases = np.random.uniform(0, 2*np.pi, N)
        
        # Coupling strength
        K = 0.7
        
        # Time step
        dt = 0.1
        
        # Create circle
        circle = Circle(radius=3, color=BLACK)
        
        #coupling_constant_text = Text(f"k:{K}")
        #kuramoto_equation = MathTex(r'\dot \theta_i = \omega_i + \frac{k}{N} \sum_{j=1}^N \sin(\theta_j - \theta_i)',fill_color=BLACK)
        #self.play(Write(kuramoto_equation))
        
        #self.add(kuramoto_equation)
        #self.wait(5)
        
        #order_param_eq = MathTex(r'R\equiv   re^{i\psi} = \frac{1}{N}\sum_{j=1}^N e^{i \theta_j}',fill_color=BLACK)
        #self.add(order_param_eq)
        
        #self.play(Transform(kuramoto_equation, order_param_eq))
        
        #self.wait(5)
        
        
        
        self.add(circle)
        
        #self.play(Transform(,circle))
        
        #self.remove(kuramoto_equation)
        #self.remove(order_param_eq)
        
        
        
        #self.remove(order_param_eq)
        
        
        
        
        # Create dots for oscillators
        dots = VGroup(*[Dot(point=np.array([
            3*np.cos(phase), 
            3*np.sin(phase), 
            0
        ]),stroke_width=5,color=self.phase_to_color(phase)) for phase in phases])
        
        self.add(dots)
        
        
        
        order_param_text = Tex(f'R: {self.calculate_order_parameter(phases):.2f}',fill_color=BLACK)
        coupling_text = Tex(f'k:{K} ',fill_color=BLACK)
        # Animate the text moving to the upper right corner
        
        
        
        #self.play(Transform(circle,coupling_text))
        #self.play(Transform(coupling_text,order_param_text))
        self.play(order_param_text.animate.to_corner(UR))
        self.play(coupling_text.animate.to_corner(UL))
        
       
        # Time evolution
        for _ in range(600):
            self.wait(dt)
            self.update_phases(phases, natural_frequencies, K, dt, N)
            self.update_dots(dots, phases)
            self.update_order_parameter_text(order_param_text, phases)
    
    def phase_to_color(self, phase):
        return interpolate_color(RED, BLUE, phase / (2 * np.pi))
    
    def update_phases(self, phases, natural_frequencies, K, dt, N):
        for i in range(N):
            interaction_sum = np.sum(np.sin(phases - phases[i]))
            phases[i] += (natural_frequencies[i] + K/N * interaction_sum) * dt

    def update_dots(self, dots, phases):
        for dot, phase in zip(dots, phases):
            dot.move_to(np.array([
                3*np.cos(phase), 
                3*np.sin(phase), 
                0
            ]))
            
            dot.set_color(self.phase_to_color(phase))

    def calculate_order_parameter(self, phases):
        N = len(phases)
        complex_order_parameter = np.sum(np.exp(1j * phases)) / N
        return np.abs(complex_order_parameter)
    
    def update_order_parameter_text(self, order_param_text, phases):
        order_param_text.become(Tex(f"R: {self.calculate_order_parameter(phases):.2f}",fill_color=BLACK).to_corner(UR))

    