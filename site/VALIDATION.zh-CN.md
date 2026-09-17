# 逐项运行验证

更新日期：2026-09-17。下表保留首次完整审计的逐项基线；新一轮完整审计已经结束并产出发现，兼容修复与专项短训练单独记录，不能当作原训练规模的完整通过。Site 会用代码摘要判断旧的完整通过证据是否仍适用于当前 Notebook。

[当前完整审计](https://github.com/azfiles/AI-For-Beginners/actions/runs/35072071135) · [全单元短训练兼容性](https://github.com/azfiles/AI-For-Beginners/actions/runs/35072489957) · [首次逐项基线报告](https://github.com/azfiles/AI-For-Beginners/actions/runs/35041992690)

| 文件 | 完整审计结果 | 补充验证或运行条件 |
| --- | --- | --- |
| [examples/01-hello-ai-world.py](../examples/01-hello-ai-world.py) | 完整执行通过 |  |
| [examples/02-simple-neural-network.py](../examples/02-simple-neural-network.py) | 完整执行通过 |  |
| [examples/03-image-classifier.ipynb](../examples/03-image-classifier.ipynb) | 完整执行通过 |  |
| [examples/04-text-sentiment.py](../examples/04-text-sentiment.py) | 完整执行通过 |  |
| [lessons/2-Symbolic/Animals.ipynb](../lessons/2-Symbolic/Animals.ipynb) | 完整执行通过 |  |
| [lessons/2-Symbolic/FamilyOntology.ipynb](../lessons/2-Symbolic/FamilyOntology.ipynb) | 完整执行通过 |  |
| [lessons/2-Symbolic/MSConceptGraph.ipynb](../lessons/2-Symbolic/MSConceptGraph.ipynb) | 未通过 | 需要 NEWSAPI_KEY 或本地标题文件；概念查询仍需网络 |
| [lessons/3-NeuralNetworks/03-Perceptron/Perceptron.ipynb](../lessons/3-NeuralNetworks/03-Perceptron/Perceptron.ipynb) | 完整执行通过 |  |
| [lessons/3-NeuralNetworks/03-Perceptron/lab/PerceptronMultiClass.ipynb](../lessons/3-NeuralNetworks/03-Perceptron/lab/PerceptronMultiClass.ipynb) | 练习准备代码通过，题目需自行完成 |  |
| [lessons/3-NeuralNetworks/04-OwnFramework/OwnFramework.ipynb](../lessons/3-NeuralNetworks/04-OwnFramework/OwnFramework.ipynb) | 完整执行通过 |  |
| [lessons/3-NeuralNetworks/04-OwnFramework/lab/MyFW_MNIST.ipynb](../lessons/3-NeuralNetworks/04-OwnFramework/lab/MyFW_MNIST.ipynb) | 练习准备代码通过，题目需自行完成 |  |
| [lessons/3-NeuralNetworks/05-Frameworks/IntroKeras.ipynb](../lessons/3-NeuralNetworks/05-Frameworks/IntroKeras.ipynb) | 完整执行通过 |  |
| [lessons/3-NeuralNetworks/05-Frameworks/IntroKerasTF.ipynb](../lessons/3-NeuralNetworks/05-Frameworks/IntroKerasTF.ipynb) | 完整执行通过 |  |
| [lessons/3-NeuralNetworks/05-Frameworks/IntroPyTorch.ipynb](../lessons/3-NeuralNetworks/05-Frameworks/IntroPyTorch.ipynb) | 完整执行通过 |  |
| [lessons/3-NeuralNetworks/05-Frameworks/lab/LabFrameworks.ipynb](../lessons/3-NeuralNetworks/05-Frameworks/lab/LabFrameworks.ipynb) | 练习准备代码通过，题目需自行完成 |  |
| [lessons/4-ComputerVision/06-IntroCV/OpenCV.ipynb](../lessons/4-ComputerVision/06-IntroCV/OpenCV.ipynb) | 完整执行通过 |  |
| [lessons/4-ComputerVision/06-IntroCV/lab/MovementDetection.ipynb](../lessons/4-ComputerVision/06-IntroCV/lab/MovementDetection.ipynb) | 练习准备代码通过，题目需自行完成 |  |
| [lessons/4-ComputerVision/07-ConvNets/ConvNetsPyTorch.ipynb](../lessons/4-ComputerVision/07-ConvNets/ConvNetsPyTorch.ipynb) | 长训练超时，未验证 |  |
| [lessons/4-ComputerVision/07-ConvNets/ConvNetsTF.ipynb](../lessons/4-ComputerVision/07-ConvNets/ConvNetsTF.ipynb) | 长训练超时，未验证 |  |
| [lessons/4-ComputerVision/07-ConvNets/lab/PetFaces.ipynb](../lessons/4-ComputerVision/07-ConvNets/lab/PetFaces.ipynb) | 练习准备代码通过，题目需自行完成 |  |
| [lessons/4-ComputerVision/08-TransferLearning/AdversarialCat_TF.ipynb](../lessons/4-ComputerVision/08-TransferLearning/AdversarialCat_TF.ipynb) | 长训练超时，未验证 |  |
| [lessons/4-ComputerVision/08-TransferLearning/Dropout.ipynb](../lessons/4-ComputerVision/08-TransferLearning/Dropout.ipynb) | 完整执行通过 |  |
| [lessons/4-ComputerVision/08-TransferLearning/TransferLearningPyTorch.ipynb](../lessons/4-ComputerVision/08-TransferLearning/TransferLearningPyTorch.ipynb) | 长训练超时，未验证 |  |
| [lessons/4-ComputerVision/08-TransferLearning/TransferLearningTF.ipynb](../lessons/4-ComputerVision/08-TransferLearning/TransferLearningTF.ipynb) | 长训练超时，未验证 |  |
| [lessons/4-ComputerVision/08-TransferLearning/lab/OxfordPets.ipynb](../lessons/4-ComputerVision/08-TransferLearning/lab/OxfordPets.ipynb) | 练习准备代码通过，题目需自行完成 |  |
| [lessons/4-ComputerVision/09-Autoencoders/AutoEncodersPyTorch.ipynb](../lessons/4-ComputerVision/09-Autoencoders/AutoEncodersPyTorch.ipynb) | 长训练超时，未验证 |  |
| [lessons/4-ComputerVision/09-Autoencoders/AutoencodersTF.ipynb](../lessons/4-ComputerVision/09-Autoencoders/AutoencodersTF.ipynb) | 长训练超时，未验证 | 全单元；128 张真实图片、每条训练路径 1 轮通过 |
| [lessons/4-ComputerVision/10-GANs/GANPyTorch.ipynb](../lessons/4-ComputerVision/10-GANs/GANPyTorch.ipynb) | 长训练超时，未验证 |  |
| [lessons/4-ComputerVision/10-GANs/GANTF.ipynb](../lessons/4-ComputerVision/10-GANs/GANTF.ipynb) | 长训练超时，未验证 | 两种架构的短训练通过 |
| [lessons/4-ComputerVision/10-GANs/StyleTransfer.ipynb](../lessons/4-ComputerVision/10-GANs/StyleTransfer.ipynb) | 长训练超时，未验证 |  |
| [lessons/4-ComputerVision/10-GANs/StyleTransfer_Keras.ipynb](../lessons/4-ComputerVision/10-GANs/StyleTransfer_Keras.ipynb) | 完整执行通过 |  |
| [lessons/4-ComputerVision/11-ObjectDetection/ObjectDetection.ipynb](../lessons/4-ComputerVision/11-ObjectDetection/ObjectDetection.ipynb) | 完整执行通过 |  |
| [lessons/4-ComputerVision/12-Segmentation/SemanticSegmentationPytorch.ipynb](../lessons/4-ComputerVision/12-Segmentation/SemanticSegmentationPytorch.ipynb) | 未通过 | 需要登记获取 PH2 数据，并设置 PH2_DATA_DIR；尚未验证 |
| [lessons/4-ComputerVision/12-Segmentation/SemanticSegmentationTF.ipynb](../lessons/4-ComputerVision/12-Segmentation/SemanticSegmentationTF.ipynb) | 未通过 | 需要登记获取 PH2 数据，并设置 PH2_DATA_DIR；尚未验证 |
| [lessons/4-ComputerVision/12-Segmentation/lab/BodySegmentation.ipynb](../lessons/4-ComputerVision/12-Segmentation/lab/BodySegmentation.ipynb) | 练习准备代码通过，题目需自行完成 |  |
| [lessons/5-NLP/13-TextRep/TextRepresentationPyTorch.ipynb](../lessons/5-NLP/13-TextRep/TextRepresentationPyTorch.ipynb) | 完整执行通过 |  |
| [lessons/5-NLP/13-TextRep/TextRepresentationTF.ipynb](../lessons/5-NLP/13-TextRep/TextRepresentationTF.ipynb) | 完整执行通过 |  |
| [lessons/5-NLP/14-Embeddings/EmbeddingsPyTorch.ipynb](../lessons/5-NLP/14-Embeddings/EmbeddingsPyTorch.ipynb) | 完整执行通过 |  |
| [lessons/5-NLP/14-Embeddings/EmbeddingsTF.ipynb](../lessons/5-NLP/14-Embeddings/EmbeddingsTF.ipynb) | 未通过 | 兼容修复复测中 |
| [lessons/5-NLP/15-LanguageModeling/CBoW-PyTorch.ipynb](../lessons/5-NLP/15-LanguageModeling/CBoW-PyTorch.ipynb) | 长训练超时，未验证 |  |
| [lessons/5-NLP/15-LanguageModeling/CBoW-TF.ipynb](../lessons/5-NLP/15-LanguageModeling/CBoW-TF.ipynb) | 长训练超时，未验证 |  |
| [lessons/5-NLP/16-RNN/RNNPyTorch.ipynb](../lessons/5-NLP/16-RNN/RNNPyTorch.ipynb) | 完整执行通过 |  |
| [lessons/5-NLP/16-RNN/RNNTF.ipynb](../lessons/5-NLP/16-RNN/RNNTF.ipynb) | 完整执行通过 |  |
| [lessons/5-NLP/17-GenerativeNetworks/GenerativePyTorch.ipynb](../lessons/5-NLP/17-GenerativeNetworks/GenerativePyTorch.ipynb) | 完整执行通过 |  |
| [lessons/5-NLP/17-GenerativeNetworks/GenerativeTF.ipynb](../lessons/5-NLP/17-GenerativeNetworks/GenerativeTF.ipynb) | 长训练超时，未验证 |  |
| [lessons/5-NLP/18-Transformers/TransformersPyTorch.ipynb](../lessons/5-NLP/18-Transformers/TransformersPyTorch.ipynb) | 长训练超时，未验证 |  |
| [lessons/5-NLP/18-Transformers/TransformersTF.ipynb](../lessons/5-NLP/18-Transformers/TransformersTF.ipynb) | 长训练超时，未验证 | 全单元；四条训练路径、每次两个真实批次通过 |
| [lessons/5-NLP/19-NER/NER-TF.ipynb](../lessons/5-NLP/19-NER/NER-TF.ipynb) | 未通过 | 修复后全单元；64 个真实句子、1 轮训练通过 |
| [lessons/5-NLP/20-LangModels/GPT-PyTorch.ipynb](../lessons/5-NLP/20-LangModels/GPT-PyTorch.ipynb) | 完整执行通过 |  |
| [lessons/6-Other/21-GeneticAlgorithms/Diophantine.ipynb](../lessons/6-Other/21-GeneticAlgorithms/Diophantine.ipynb) | 仅说明，无代码 |  |
| [lessons/6-Other/21-GeneticAlgorithms/Genetic.ipynb](../lessons/6-Other/21-GeneticAlgorithms/Genetic.ipynb) | 完整执行通过 |  |
| [lessons/6-Other/22-DeepRL/CartPole-RL-PyTorch.ipynb](../lessons/6-Other/22-DeepRL/CartPole-RL-PyTorch.ipynb) | 完整执行通过 |  |
| [lessons/6-Other/22-DeepRL/CartPole-RL-TF.ipynb](../lessons/6-Other/22-DeepRL/CartPole-RL-TF.ipynb) | 完整执行通过 |  |
| [lessons/6-Other/22-DeepRL/lab/MountainCar.ipynb](../lessons/6-Other/22-DeepRL/lab/MountainCar.ipynb) | 练习准备代码通过，题目需自行完成 |  |
| [lessons/6-Other/22-DeepRL/notebook.ipynb](../lessons/6-Other/22-DeepRL/notebook.ipynb) | 未通过 | 兼容修复复测中 |
| [lessons/6-Other/22-DeepRL/tmp.ipynb](../lessons/6-Other/22-DeepRL/tmp.ipynb) | 完整执行通过 |  |
| [lessons/X-Extras/X1-MultiModal/Clip.ipynb](../lessons/X-Extras/X1-MultiModal/Clip.ipynb) | 完整执行通过 |  |
