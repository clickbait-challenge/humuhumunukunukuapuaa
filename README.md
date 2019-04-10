# :arrow_down: AppliedNLP Paper Reproduction :arrow_down:
## ["Detecting Clickbait in Online Social Media: You Won’t Believe How We Did It"](https://arxiv.org/pdf/1710.06699.pdf)

Code for Group 26 python implementation of Applied NLP project IN4325 :tropical_fish:.

Team members:

 * [Andrei Simion-Constantinescu](https://www.linkedin.com/in/andrei-simion-constantinescu/)
 * [Nele Albers](https://github.com/nelealbers)
 * [Mihai Voicescu](https://github.com/mihai1voicescu)
 * [Lorena Poenaru-Olaru](https://github.com/LorenaPoenaru)

## Data :floppy_disk:

For training and testing the models, we used the Clickbait Challenge labeled datasets that can be obtained from the [Clickbait Challenge official site](https://www.clickbait-challenge.org/#data). Moreover, GloVe Twitter trained word embeddings needs to be downloaded from [pymagnitude GitHub page](https://github.com/plasticityai/magnitude). 

Our custom Twitter clickBaits posts can be downloaded from this [link](https://drive.google.com/file/d/1x7vv7VFEw6nMuuLEm7DNo3NkPWA43JGS/view?usp=sharing). 

## Project structure :open_file_folder:

The project tree is displayed bellow:
<pre>
root
│   
│   generate_features.py            computes the features and saves them as a dataframes (needs running Stanford NLP java server) 
|   run_hyperparams_gridsearch.py   performs randomized grid-search for finding model's best hyperparams
|   run_tests.py                    tests models with simple and combining classifiers for small, large and custom data
|   make_score_dist.py              plots clickBait scores histograms for small and large dataset		          
|   make_tsne.py                    compute t-SNE to reduce 100d sentence vectors to 2D and plots scatterplot of sentences			
|   mutual_info.py                  calculates feature importance before training on the other features apart sentence embeds			
|   feature_imp.py                  computes feature importance after training using information gain for all features apart embeds		
|   group_imp.py                    computes feature group importance on trained models			
|   make_confmat.py                 plots confusion matrix for predicted values based on trained models				
|   logger.py                       logging system for generating folders initial structure and saving application logs to HTML files
|   config.txt                      application configuration file 
|
└───features   original, POS tags and sentence structure computed using Stanford NLP server, sentence structure features and word embeds
|
|   original_features.py
|   pos_tags_features.py
|   sentence_sentm_features.py
|   sentence_struct_features.py
|   sentence_word_emb.py
|
└───hyperparams       with randomized grid search class and hyperparameters search grid values for each classifier
|
└───utils             with the wrapper class for calling Stanford NLP java server and utility reading, splitting and concatenate data
|
└───crawler           JavaScript crawler for collecting our own <b>custom</b> clickBait tweets
|
└───data
|   |
│   │   small/large/custom_original.csv
|   |   small/large/custom_train.csv     
│   │   Downworthy.txt
|   |   sentiment.csv
│   │   dialog_dataset.csv
|   |   glove.twitter.27B.100d.magnitude    <b>!</b> needs to be downloaded 
|   |
│   └───small     <b>!</b> needs to be downloaded 
|   |   media/
|   |   instances.jsonl
|   |   truth.jsonl
|   |
|   └───large     <b>!</b> needs to be downloaded  same layout as <b>small</b>
|   └───custom    <b>!</b> needs to be downloaded  same layout as <b>small</b>
|
└───logs
|   |   Log files in HTML format for 
|   |   	hyperparams search, training and testing simple and ensembles models, compute importance of features a.s.o
|   └───
|
└───models
|   |
|   └───small
|   └───large
|   └───custom
|   |
│   │   Saved hyperparamaters after randomize grid search for Decision Tree, AdaBoost, Random Forest, XGBoost
│   |  
│   │   Saved trained ensemble models as pickle files (NOT all pushed to GitHub due to space issue) 
│   └───
|
└───output
    │   Plots with clickBait scores distributions, tSNE scatterplot before training
    │   
    │   Plot with confusion matrix, barplots for feature importance after training 
    |
    |   Csv's files with feature importance before and after trainining normalized scores    
    |  
    |   tSNE reduced to 2D sentence vectors as .npy files
    └───
</pre>

> :exclamation: Do not forget to add the files downloaded in the previous section in the right folders according to the project structure

## Config file :bookmark_tabs:

```
{
	"SMALL_DATA_FOLDER": "small",
	"SMALL_DATA_FILE": "instances.jsonl",
	"SMALL_TARGETS_FILE": "truth.jsonl",
	"LARGE_DATA_FOLDER": "large",
	"LARGE_DATA_FILE": "instances.jsonl",
	"LARGE_TARGETS_FILE": "truth.jsonl",
	"CUSTOM_DATA_FOLDER": "custom",
	"CUSTOM_DATA_FILE": "twitter-out2019-04-06T12_10_16.106Z.jsonl",
	"CUSTOM_TARGETS_FILE": "truth.jsonl",
	"DOWNWORTHY_FILE" : "Downworthy.txt",
	"GLOVE_FILE": "glove.twitter.27B.100d.magnitude",
	"EMB_SIZE": "100",
	"BEST_ADA_S": "AdaBoostClassifier_params_2019-04-06_15_24_04.json",
	"BEST_RANDF_S": "RandomForestClassifier_params_2019-04-06_15_28_01.json",
	"BEST_DECT_S": "DecisionTreeClassifier_params_2019-04-06_15_23_06.json",
	"BEST_XGB_S": "XGBClassifier_params_2019-04-06_15_28_33.json",
	"BEST_ADA_L": "AdaBoostClassifier_params_2019-04-06_15_41_20.json",
	"BEST_RANDF_L": "RandomForestClassifier_params_2019-04-06_16_28_13.json",
	"BEST_DECT_L": "DecisionTreeClassifier_params_2019-04-06_15_30_59.json",
	"BEST_XGB_L": "XGBClassifier_params_2019-04-06_16_33_33.json",
	"SMALL_BEST": "RandomForestClassifier_0.0423.pkl",
	"LARGE_BEST": "VotingClassifier_0.0957.pkl",	
}
```

## Installation :computer:
The scripts can be run in [Anaconda](https://www.anaconda.com/download/) Windows/Linux environment.

You need to create an Anaconda :snake: `python 3.6` environment named `app_nlp`.
Inside that environment some addition packages needs to be installed. Run the following commands inside Anaconda Prompt ⌨:
```shell
(base) conda create -n app_nlp python=3.6 anaconda
(base) conda activate app_nlp
(app_nlp) pip install vaderSentiment #vaderSentiment 3.2.1
(app_nlp) conda install -c anaconda py-xgboost #xgboost 0.8.0 
(app_nlp) pip install pymagnitude #pymagnitude 0.1.120
(app_nlp) pip install pytesseract #pytesseract 0.2.6
```

We will also need to download `stopwords`, `opinion_lexicon` and `wordnet` from `nltk` ⌨:
```python
import nltk
nltk.download('stopwords')
nltk.download('opinion_lexicon')
nltk.download('wordnet')
```

The files downloaded at [Data section](#data) needs to be places in the right folders according to the [Project structure](#project-structure).

Moreover, [Stanford CoreNLP `jars`](https://stanfordnlp.github.io/CoreNLP/) needs to be downloaded in order to launch the java server required for running `generate_features.py`.

Furthermore, tesseract needs to be installed (following this [instructions](https://github.com/tesseract-ocr/tesseract/wiki)) and added to `PATH` enviroment variable.

## Usage :arrow_forward:

Before running `generate_features.py`, a CoreNLP server needs to be launched from terminal. On the same level as the unzipped Stanford java server, run the following command ⌨:
```shell
java -mx1024m -cp "stanford-corenlp-full-2018-10-05/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \\ 
-preload tokenize,ssplit,pos,parse,depparse -status_port 9000 -port 9000 -timeout 300000
```

The importance scripts apart the ones that genearates plots or computes feature importances are `generate_features.py` and `run_tests.py`. Both can be runned inside the enviroment created at [Installation section](#installation) :rocket: :
```shell
(base) conda activate app_nlp
(app_nlp) python generate_features.py
(app_nlp) python run_tests.py
```

## TIRA run :trophy:

The output from one of our TIRA submission can be visualized [here](_tira_results/TIRA_output.html).

The results from one of our TIRA submission can be visualized [here](_tira_results/TIRA_results.html).