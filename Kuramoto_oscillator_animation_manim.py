from manim import *
import numpy as np

class KuramotoOscillators(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        
        # Number of oscillators
        N = 20
        
        # Initialize random natural frequencies and phases
        natural_frequencies = np.random.uniform(0.8, 1.5, N)
        phases = np.random.uniform(0, 2 * np.pi, N)
        
        # Coupling strength
        K = 0.7
        
        # Time step for simulation
        dt = 0.1
        
        # Create and add the main circle to the scene
        circle = Circle(radius=3, color=BLACK)
        self.add(circle)
        
        # Create and add dots representing oscillators
        dots = VGroup(*[Dot(
            point=np.array([3 * np.cos(phase), 3 * np.sin(phase), 0]),
            stroke_width=5,
            color=self.phase_to_color(phase)
        ) for phase in phases])
        self.add(dots)
        
        # Initialize and position the order parameter and coupling text
        order_param_text = Tex(f'R: {self.calculate_order_parameter(phases):.2f}', fill_color=BLACK)
        coupling_text = Tex(f'k: {K}', fill_color=BLACK)
        
        self.play(order_param_text.animate.to_corner(UR))
        self.play(coupling_text.animate.to_corner(UL))
        
        # Time evolution of the system
        for _ in range(600):
            self.wait(dt)
            self.update_phases(phases, natural_frequencies, K, dt, N)
            self.update_dots(dots, phases)
            self.update_order_parameter_text(order_param_text, phases)
    
    def phase_to_color(self, phase):
        """Converts a phase to a color ranging from RED to BLUE."""
        return interpolate_color(RED, BLUE, phase / (2 * np.pi))
    
    def update_phases(self, phases, natural_frequencies, K, dt, N):
        """Updates the phases of the oscillators based on the Kuramoto model."""
        for i in range(N):
            interaction_sum = np.sum(np.sin(phases - phases[i]))
            phases[i] += (natural_frequencies[i] + K / N * interaction_sum) * dt

    def update_dots(self, dots, phases):
        """Updates the positions and colors of the dots representing the oscillators."""
        for dot, phase in zip(dots, phases):
            dot.move_to(np.array([
                3 * np.cos(phase), 
                3 * np.sin(phase), 
                0
            ]))
            dot.set_color(self.phase_to_color(phase))

    def calculate_order_parameter(self, phases):
        """Calculates the order parameter R, a measure of synchronization."""
        N = len(phases)
        complex_order_parameter = np.sum(np.exp(1j * phases)) / N
        return np.abs(complex_order_parameter)
    
    def update_order_parameter_text(self, order_param_text, phases):
        """Updates the text displaying the order parameter."""
        order_param_text.become(
            Tex(f"R: {self.calculate_order_parameter(phases):.2f}", fill_color=BLACK).to_corner(UR)
        )
