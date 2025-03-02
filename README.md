**Joint Entity and Relationship Extraction for Safety Risk Analysis in Shield Tunnelling**

This repository contains the implementation and results of a joint entity and relationship extraction model designed to analyze safety risks in shield tunnelling. The model integrates advanced deep learning techniques to address the complexity of safety risk management in shield tunnelling environments.

**Problem Statement**

Shield tunnelling is characterized by its complexity, confined working environments, and the parallel execution of construction activities. The spatiotemporal coupling of various safety risks introduces additional challenges, leading to frequent accidents and limiting the accuracy of risk inference and assessment. Previous studies have insufficiently utilized large-scale textual data from accident cases, resulting in incomplete understanding of the spatiotemporal coupling and evolution patterns of construction safety risks.

**Methodology**

To address this research gap, we developed a joint entity and relationship extraction model by integrating the following components:
BERT (Bidirectional Encoder Representations from Transformers): Captures contextual semantics of risk factors.
BiLSTM (Bidirectional Long Short-Term Memory): Models sequential dependencies in the data.
Multi-Head Attention Mechanism: Enhances the model's ability to focus on relevant features.
Densely Connected Graph Convolutional Networks (DCGCN): Captures topological relationships between risk factors.
The model, named BBi-MA-DCGCN, comprehensively extracts entities and relationships from textual data related to shield tunnelling accidents. The extracted results are used to construct a risk-coupled evolutionary knowledge graph, which integrates knowledge querying and path reasoning methods to infer the spatiotemporal coupling and evolution of safety risks.

**Data and Results Sharing**

Due to confidentiality agreements with data providers (e.g., China Communications Construction Group), the full dataset cannot be publicly released. However, the entity and relationship recognition results obtained from the processed and standardized data are shared via this GitHub repository. These results provide insights into the spatiotemporal coupling and evolution patterns of safety risks in shield tunnelling.

**Usage**

Entity and Relationship Extraction: The model can be used to extract entities and relationships from textual data related to shield tunnelling accidents.
Knowledge Graph Construction: The extracted results can be used to construct a risk-coupled evolutionary knowledge graph for further analysis.
Risk Assessment: The interaction matrix (IM) principle can be applied to quantitatively assess risk factors based on the knowledge graph framework.

**Conclusion**

This study provides a novel theoretical framework and technical pathway for understanding the spatiotemporal coupling evolution mechanism of safety risks in shield tunnelling. The results significantly enhance the accuracy of risk identification, dynamic inference, and quantitative evaluation, offering innovative solutions for risk control in complex construction environments.
