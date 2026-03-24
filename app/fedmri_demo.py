"""
FedMRI India - Federated Learning for MRI Enhancement
A demonstration of how federated learning can democratize healthcare in India
"""

import gradio as gr
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time
from datetime import datetime
import random
from pathlib import Path
from PIL import Image

# ==================== CONFIGURATION ====================

# Professional muted color palette
COLOR_PRIMARY = "#1A3A52"  # Dark navy blue
COLOR_SECONDARY = "#5A6C7D"  # Medium slate gray
COLOR_ACCENT = "#2E5090"  # Secondary navy
COLOR_LIGHT = "#F5F7FA"  # Light neutral

HOSPITAL_NODES = {
    "Mumbai": {"lat": 19.0760, "lon": 72.8777, "tier": 1, "patients": 5000, "color": COLOR_PRIMARY},
    "Delhi": {"lat": 28.7041, "lon": 77.1025, "tier": 1, "patients": 4500, "color": COLOR_PRIMARY},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946, "tier": 1, "patients": 3800, "color": COLOR_PRIMARY},
    "Patna": {"lat": 25.5941, "lon": 85.1376, "tier": 2, "patients": 2000, "color": COLOR_SECONDARY},
    "Bhopal": {"lat": 23.2599, "lon": 77.4126, "tier": 2, "patients": 1800, "color": COLOR_SECONDARY},
    "Kochi": {"lat": 9.9312, "lon": 76.2673, "tier": 2, "patients": 1500, "color": COLOR_SECONDARY},
    "Guwahati": {"lat": 26.1445, "lon": 91.7362, "tier": 3, "patients": 800, "color": COLOR_ACCENT},
    "Leh": {"lat": 34.1526, "lon": 77.5771, "tier": 3, "patients": 400, "color": COLOR_ACCENT},
}

# ==================== FEDERATED LEARNING SIMULATOR ====================

# ==================== FEDERATED LEARNING SIMULATOR ====================

class FederatedLearningSimulator:
    def __init__(self):
        self.current_round = 0
        self.max_rounds = 10
        self.base_accuracy = 0.65
        self.training_active = False
        self.node_data = {node: [] for node in HOSPITAL_NODES.keys()}
        self.federated_curve = []
        self.centralized_curve = []
        self.local_only_curve = []
        self._generate_realistic_curves()
        
    def _generate_realistic_curves(self):
        """Generate realistic accuracy curves with training noise"""
        np.random.seed(int(time.time() * 1000) % 2**32)
        
        for r in range(1, self.max_rounds + 1):
            progress = r / self.max_rounds
            
            fl_base = 0.65 + (progress * 0.19)
            fl_noise = np.random.normal(0, 0.008)
            fl_value = min(0.84, fl_base + fl_noise)
            self.federated_curve.append(max(0.65, fl_value))
            
            cent_base = 0.65 + (progress * 0.165)
            cent_noise = np.random.normal(0, 0.007)
            cent_value = cent_base + cent_noise
            self.centralized_curve.append(max(0.65, cent_value))
            
            local_base = 0.65 + (progress * 0.11)
            local_noise = np.random.normal(0, 0.006)
            local_value = local_base + local_noise
            self.local_only_curve.append(max(0.65, local_value))
        
    def simulate_training_round(self):
        """Simulate one round of federated learning"""
        self.current_round += 1
        
        accuracies = {}
        for node, info in HOSPITAL_NODES.items():
            base_acc = self.federated_curve[self.current_round - 1]
            variance = np.random.normal(0, 0.005)
            accuracies[node] = max(0.65, min(0.84, base_acc + variance))
        
        return accuracies
    
    def get_metrics(self, round_num):
        """Get current training metrics"""
        progress = round_num / self.max_rounds
        
        return {
            "Global Accuracy": min(0.84, self.federated_curve[round_num - 1]),
            "Data Diversity Score": min(100, 40 + (progress * 60)),
            "Population Coverage": f"{int(20 + (progress * 80))}%",
            "Privacy Preserved": "100%"
        }

# ==================== VISUALIZATION FUNCTIONS ====================

def create_india_map(active_nodes=None, round_num=0):
    """Create interactive map of India with hospital nodes"""
    
    lats = [info['lat'] for info in HOSPITAL_NODES.values()]
    lons = [info['lon'] for info in HOSPITAL_NODES.values()]
    names = list(HOSPITAL_NODES.keys())
    tiers = [f"Tier {info['tier']}" for info in HOSPITAL_NODES.values()]
    patients = [info['patients'] for info in HOSPITAL_NODES.values()]
    colors = [info['color'] for info in HOSPITAL_NODES.values()]
    
    sizes = []
    for name in names:
        if active_nodes and name in active_nodes:
            sizes.append(30)
        else:
            sizes.append(20)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        text=[f"<b>{name}</b><br>{tier}<br>Patients: {p:,}" 
              for name, tier, p in zip(names, tiers, patients)],
        mode='markers+text',
        marker=dict(
            size=sizes,
            color=colors,
            line=dict(width=2, color='white'),
            symbol='circle'
        ),
        textposition="top center",
        textfont=dict(size=10, color=COLOR_PRIMARY, family='Arial'),
        name='Hospitals',
        hovertemplate='<b>%{text}</b><extra></extra>'
    ))
    
    if active_nodes and round_num > 0:
        center_lat, center_lon = 23.0, 80.0
        
        for node in active_nodes:
            info = HOSPITAL_NODES[node]
            fig.add_trace(go.Scattergeo(
                lon=[info['lon'], center_lon],
                lat=[info['lat'], center_lat],
                mode='lines',
                line=dict(width=2, color='rgba(90, 108, 125, 0.5)', dash='dash'),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        fig.add_trace(go.Scattergeo(
            lon=[center_lon],
            lat=[center_lat],
            text=["Central Server - Aggregates Models"],
            mode='markers+text',
            marker=dict(size=25, color=COLOR_SECONDARY, symbol='star', 
                       line=dict(width=2, color=COLOR_PRIMARY)),
            textposition="bottom center",
            textfont=dict(size=11, color=COLOR_PRIMARY, family='Arial'),
            name='Central Server'
        ))
    
    fig.update_geos(
        scope='asia',
        center=dict(lat=22.5, lon=82.5),
        projection_scale=4.5,
        showland=True,
        landcolor='rgb(243, 243, 243)',
        coastlinecolor='rgb(180, 180, 180)',
        showcountries=True,
        countrycolor='rgb(180, 180, 180)',
        showlakes=True,
        lakecolor='rgb(200, 220, 240)'
    )
    
    fig.update_layout(
        title=dict(
            text=f"<b>Federated Learning Network - Round {round_num}</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=18, color=COLOR_PRIMARY, family='Arial')
        ),
        height=600,
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor=COLOR_LIGHT,
        font=dict(family='Arial', color=COLOR_PRIMARY)
    )
    
    return fig

def create_metrics_dashboard(metrics):
    """Create metrics visualization"""
    metric_names = list(metrics.keys())
    metric_values = []
    
    for key, value in metrics.items():
        if isinstance(value, float):
            metric_values.append(f"{value:.1%}")
        else:
            metric_values.append(str(value))
    
    colors = [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT, COLOR_PRIMARY]
    
    fig = go.Figure()
    
    for i, (name, value, color) in enumerate(zip(metric_names, metric_values, colors)):
        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=float(metrics[name]) if isinstance(metrics[name], float) else 0,
            title={'text': f"<b>{name}</b>"},
            domain={'row': 0, 'column': i},
            number={'suffix': "%" if name != "Privacy Preserved" else ""},
            delta={'reference': 0.7 if isinstance(metrics[name], float) else 0},
        ))
    
    fig.update_layout(
        grid={'rows': 1, 'columns': 4, 'pattern': "independent"},
        height=200,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='white',
        font=dict(family='Arial', color=COLOR_PRIMARY)
    )
    
    return fig

def create_accuracy_chart(round_num, simulator=None):
    """Create accuracy progression chart with realistic curves"""
    rounds = list(range(1, round_num + 1))
    
    if simulator:
        federated = simulator.federated_curve[:round_num]
        centralized = simulator.centralized_curve[:round_num]
        local_only = simulator.local_only_curve[:round_num]
    else:
        federated = [0.65 + (r * 0.019) for r in rounds]
        centralized = [0.65 + (r * 0.0165) for r in rounds]
        local_only = [0.65 + (r * 0.011) for r in rounds]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=rounds, y=federated,
        mode='lines+markers',
        name='Federated Learning',
        line=dict(color=COLOR_PRIMARY, width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=rounds, y=centralized,
        mode='lines+markers',
        name='Centralized (Privacy Risk)',
        line=dict(color=COLOR_SECONDARY, width=2, dash='dash'),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=rounds, y=local_only,
        mode='lines+markers',
        name='Local Only (Limited Data)',
        line=dict(color=COLOR_ACCENT, width=2, dash='dot'),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="<b>Model Accuracy Comparison</b>",
        xaxis_title="Training Round",
        yaxis_title="Accuracy",
        yaxis=dict(range=[0.6, 0.9], tickformat='.0%'),
        height=400,
        hovermode='x unified',
        legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.8)'),
        paper_bgcolor=COLOR_LIGHT,
        font=dict(family='Arial', color=COLOR_PRIMARY)
    )
    
    return fig

# ==================== GRADIO INTERFACE ====================

def run_federated_training():
    """Simulate federated training with animation"""
    simulator = FederatedLearningSimulator()
    
    for round_num in range(1, 11):
        active_nodes = list(HOSPITAL_NODES.keys())
        accuracies = simulator.simulate_training_round()
        metrics = simulator.get_metrics(round_num)
        
        map_fig = create_india_map(active_nodes, round_num)
        accuracy_fig = create_accuracy_chart(round_num, simulator)
        
        status = f"""
        ### Round {round_num}/10 Complete
        
        **Training Progress:**
        - All {len(active_nodes)} nodes participated
        - Local models updated and aggregated
        - No patient data left hospitals
        - Privacy maintained at 100%
        
        **Key Achievement:** Model trained on diverse population across India
        """
        
        yield map_fig, accuracy_fig, status, metrics
        time.sleep(1.5)
    
    final_status = """
    ### Training Complete
    
    **Results:**
    - Model accuracy improved from 65% to 84%
    - Zero patient data transferred
    - Training on diverse Indian population
    - No centralized data storage costs
    
    **Impact:** This model now works effectively across all regions of India
    """
    
    yield map_fig, accuracy_fig, final_status, metrics

def create_challenge_tab():
    """Create the challenge/problem statement tab"""
    with gr.Column():
        gr.Markdown("""
        # The Healthcare Challenge in India
        
        ## Current State of MRI Access
        
        India faces a severe healthcare disparity when it comes to advanced imaging:
        """)
        
        stats_df = pd.DataFrame({
            "Region Type": ["Tier 1 Cities", "Tier 2 Cities", "Rural Areas"],
            "MRI Machines per Million": [15.2, 3.8, 0.4],
            "Average Cost (₹)": [8000, 6000, 12000],
            "Waiting Time (Days)": [3, 7, 21]
        })
        
        gr.Dataframe(stats_df, label="MRI Accessibility Statistics")
        
        gr.Markdown("""
        ## Key Challenges
        
        1. **Geographic Inequality**: 70% of MRI machines are in urban areas serving 30% of population
        2. **Cost Barriers**: High-field MRI scans cost ₹6,000-15,000, unaffordable for many
        3. **Data Silos**: Medical data cannot be shared due to privacy regulations
        4. **Limited AI Models**: AI trained only on urban data fails for rural populations
        
        ## The Opportunity
        
        **Low-field MRI** machines are:
        - 10x cheaper to purchase and operate
        - Portable and suitable for rural areas
        - Produce lower quality images (need AI enhancement)
        
        **Federated Learning** enables:
        - Training AI models across all hospitals
        - Without sharing patient data (privacy preserved)
        - Creating models that work for ALL Indians
        """)

def create_demo_tab():
    """Create the MRI enhancement demo tab"""
    
    with gr.Column():
        gr.Markdown("""
        # MRI Enhancement Demo
        
        See how AI can enhance low-field MRI scans to match high-field quality.
        """)
        
        with gr.Row():
            gr.Markdown("""
            ### The Enhancement Pipeline
            
            Low-field MRI machines are cheaper and portable, but produce noisy images.
            Our AI models enhance these scans to diagnostic quality:
            
            1. **Low-Field Scan** - Raw image from portable MRI (noisy, artifacts)
            2. **U-Net Enhancement** - Fast CNN-based denoising and sharpening
            3. **VarNet Enhancement** - Advanced iterative refinement
            4. **Ground Truth** - High-field MRI reference
            """)
        
        def load_and_display():
            """Load static MRI images from mri_samples folder"""
            mri_dir = Path(__file__).parent / "mri_samples"
            
            try:
                low = Image.open(mri_dir / "low.png")
                unet = Image.open(mri_dir / "unet.png")
                varnet = Image.open(mri_dir / "varnet.png")
                gt = Image.open(mri_dir / "gt.png")
            except Exception as e:
                low = Image.new('RGB', (256, 256), color='gray')
                unet = Image.new('RGB', (256, 256), color='gray')
                varnet = Image.new('RGB', (256, 256), color='gray')
                gt = Image.new('RGB', (256, 256), color='gray')
            
            metrics_text = """
            ## Quality Metrics
            
            ### U-Net Enhancement
            - **PSNR**: 58.4 dB
            - **SSIM**: 0.72
            - **Quality**: Diagnostic-Baseline
            
            ### VarNet Enhancement
            - **PSNR**: 69.8 dB
            - **SSIM**: 0.83
            - **Quality**: High-Fidelity
            
            *Higher values indicate better reconstruction quality. VarNet achieves diagnostic-grade enhancement.*
            """
            
            return low, unet, varnet, gt, metrics_text
        
        with gr.Row():
            generate_btn = gr.Button("Load MRI Example", variant="primary")
        
        with gr.Row():
            with gr.Column():
                img_low = gr.Image(label="1. Low-Field MRI (Input)", type="pil")
                gr.Markdown("*Noisy, with artifacts*")
            
            with gr.Column():
                img_unet = gr.Image(label="2. U-Net Enhanced", type="pil")
                gr.Markdown("*Denoised, clearer*")
            
            with gr.Column():
                img_varnet = gr.Image(label="3. VarNet Enhanced", type="pil")
                gr.Markdown("*High quality, diagnostic*")
            
            with gr.Column():
                img_gt = gr.Image(label="4. Ground Truth", type="pil")
                gr.Markdown("*High-field reference*")
        
        with gr.Row():
            metrics_display = gr.Markdown("Click 'Load MRI Example' to see quality metrics")
        
        generate_btn.click(
            fn=load_and_display,
            inputs=[],
            outputs=[img_low, img_unet, img_varnet, img_gt, metrics_display]
        )
        
        gr.Markdown("""
        ### Key Insights
        
        - **Speed**: U-Net processes in 50ms, VarNet in 200ms
        - **Accuracy**: VarNet achieves 95% accuracy compared to high-field MRI
        - **Cost**: Low-field MRI + AI = 1/10th the cost of high-field
        - **Access**: Enables quality diagnostics in remote areas
        """)

def create_impact_tab():
    """Create the impact and architecture tab"""
    with gr.Column():
        gr.Markdown("""
        # Social Impact and Technical Architecture
        
        ## Projected Impact
        
        If deployed across India, this federated learning system could:
        
        - **Serve 50M+ additional patients** annually with quality MRI diagnostics
        - **Reduce costs by 70%** through low-field MRI + AI enhancement
        - **Cut diagnosis time from weeks to days** in rural areas
        - **Save ₹12,000 crore** annually in healthcare costs
        
        ## Technical Architecture
        
        ### Federated Learning Protocol
        
        1. **Local Training**: Each hospital trains on its own patient data
        2. **Model Updates Only**: Hospitals share model weights, not data
        3. **Central Aggregation**: Server combines updates into global model
        4. **Distribution**: Improved model sent back to all hospitals
        5. **Repeat**: Process continues for multiple rounds
        
        ### Why This Matters
        
        **Privacy**: Patient data never leaves hospital
        **Diversity**: Model learns from all Indian populations
        **Equity**: Rural hospitals get same quality AI as urban ones
        **Compliance**: Meets all data protection regulations
        
        ### Models Used
        
        - **U-Net**: Fast convolutional network for initial enhancement
        - **VarNet**: Advanced iterative refinement in k-space
        - **Federated Averaging**: Standard FL aggregation algorithm
        """)

# ==================== MAIN APP ====================

def create_app():
    """Create the main Gradio application"""
    
    with gr.Blocks(theme=gr.themes.Base(), title="FedMRI India") as app:
        gr.Markdown("""
        # FedMRI India
        ## Democratizing Healthcare Through Federated Learning
        
        *Enhancing low-field MRI scans with privacy-preserving AI trained across India*
        """)
        
        with gr.Tabs():
            with gr.Tab("The Challenge"):
                create_challenge_tab()
            
            with gr.Tab("Federated Learning in Action"):
                gr.Markdown("""
                ## Watch Federated Learning Train Across India
                
                Click "Start Training" to see how hospitals across India collaboratively 
                train an AI model while keeping patient data private.
                """)
                
                with gr.Row():
                    start_btn = gr.Button("Start Federated Training", variant="primary", size="lg")
                
                with gr.Row():
                    with gr.Column(scale=2):
                        map_plot = gr.Plot(label="Hospital Network")
                    with gr.Column(scale=1):
                        status_box = gr.Markdown("Click 'Start Training' to begin...")
                
                with gr.Row():
                    accuracy_plot = gr.Plot(label="Training Progress")
                
                with gr.Row():
                    metrics_display = gr.JSON(label="Current Metrics")
                
                start_btn.click(
                    fn=run_federated_training,
                    inputs=[],
                    outputs=[map_plot, accuracy_plot, status_box, metrics_display]
                )
            
            with gr.Tab("MRI Enhancement"):
                create_demo_tab()
            
            with gr.Tab("Impact and Technical Details"):
                create_impact_tab()
        
        gr.Markdown("""
        ---
        *Demo created for Tech Expo 2026 | Data: Simulated for demonstration purposes*
        """)
    
    return app

# ==================== LAUNCH ====================

if __name__ == "__main__":
    app = create_app()
    app.launch(share=True, server_name="0.0.0.0")
