import pandas
import os
import numpy as np
import matplotlib.pyplot as plt
import hdbscan
from sklearn import linear_model
from sklearn.preprocessing import Imputer
from sklearn.metrics import mean_squared_error
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import seaborn

def readData():
    currentDir = os.getcwd()
    path = os.path.join(currentDir, "data" + os.sep +"formant-data-f0.xlsx")
    df = pandas.read_excel(path)
    return df


#Train model to fit x -> y
def model1(df_X, df_Y):

    # Get the readings that are good in both
    good_x = df_X["include"] == 1
    good_y = df_X["include"] == 1
    good = good_x & good_y 

    df_X_good = df_X[good]
    df_Y_good = df_Y[good]

    X = df_X_good[["F1", "F2"]].values
    y = df_Y_good[["F1", "F2"]].values

    model = linear_model.LinearRegression()
    #model = DecisionTreeRegressor(max_depth=5)

    # Split into train and test set (Dont see why we would need validation since we have no hyperparameters)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Predict (Should do on only test set)
    prediction = model.predict(X_test)

    # Get error score
    print("Mean squared error before regression was", mean_squared_error(y, X))
    print("Mean squared error after regression is", mean_squared_error(y_test, prediction))

    return model

def saveDFs(df_B, df_J, df_O):
    writer = pandas.ExcelWriter("test.xlsx")
    df_B.to_excel(writer, 'B')
    df_J.to_excel(writer, 'J')
    df_O.to_excel(writer, 'O')
    writer.save()

# Imput mean for missing F2s
def imput(df):
    imputer = Imputer(missing_values='NaN', strategy='mean', axis=0)
    df["F2"]=imputer.fit_transform(df[["F2"]]).ravel()

#
def cluster(df_B, df_J, df_O):
    df_B_clean = df_B[df_B["include"] == 1]
    df_J_clean = df_J[df_J["include"] == 1]
    df_O_clean = df_O[df_O["include"] == 1]

    #df_B_clean = df_B_clean[df_B_clean["label"].isin(["A:", "i:", "o:", "u:", "e:"])]
    #df_J_clean = df_J_clean[df_J_clean["label"].isin(["A:", "i:", "o:", "u:", "e:"])]
    #df_O_clean = df_O_clean[df_O_clean["label"].isin(["A:", "i:", "o:", "u:", "e:"])]
    
    #print(df_B_clean[df_B_clean["label"] == "A:"])
    #print("F1", df_B_clean[df_B_clean["label"] == "A:"]["F1"])

    X_O = df_O_clean[["F1", "F2"]].values
    X_B = df_B_clean[["F1", "F2"]].values
    X_J = df_J_clean[["F1", "F2"]].values

    #Bark conversion
    X_O = (26.81*X_O)/(1960+X_O)-0.53
    X_B = (26.81*X_B)/(1960+X_B)-0.53
    X_J = (26.81*X_J)/(1960+X_J)-0.53

    # print("running tsne")
    # tsne = TSNE(n_components=2, random_state=0, perplexity=35)
    # xo = tsne.fit_transform(X_O)
    # xb = tsne.fit_transform(X_B)
    # xj = tsne.fit_transform(X_J)

    xo = X_O
    xj = X_J
    xb = X_B

    # print("clustering")
    # clusterer = hdbscan.HDBSCAN(min_cluster_size=10)
    # lo = clusterer.fit_predict(xo)
    # lj = clusterer.fit_predict(xj)
    # lb = clusterer.fit_predict(xb)

    # clusterer = KMeans(n_clusters=4)
    # lo = clusterer.fit_predict(xo)
    # lj = clusterer.fit_predict(xj)
    # lb = clusterer.fit_predict(xb)


    print("Plotting data")
    fig1 = plt.figure(None)
    ax1 = fig1.add_subplot(1,3,1) 
    ax1.set_xlabel('F2 (Bark)', fontsize = 15)
    ax1.set_ylabel('F1 (Bark)', fontsize = 15)
    ax1.set_title("O", fontsize = 20)

    ax1.scatter(xo[:,1]
                , xo[:,0]
                , c=df_O_clean["nr_label"]
                , s = 10)

    
    ax1.grid()
    ax1.set_ylim([1, 10])
    ax1.set_xlim([5, 14])
    plt.gca().invert_yaxis()
    plt.gca().invert_xaxis()
    

    ax2 = fig1.add_subplot(1,3,2) 
    ax2.set_xlabel('F2 (Bark)', fontsize = 15)
    ax2.set_ylabel('F1 (Bark)', fontsize = 15)
    ax2.set_title("J", fontsize = 20)

    ax2.scatter(xj[:,1]
                , xj[:,0]
                , c=df_J_clean["nr_label"]
                , s = 10)

    
    ax2.grid()
    ax2.set_ylim([1, 10])
    ax2.set_xlim([5, 14])
    plt.gca().invert_yaxis()
    plt.gca().invert_xaxis()
    
    ax3 = fig1.add_subplot(1,3,3) 
    ax3.set_xlabel('F2 (Bark)', fontsize = 15)
    ax3.set_ylabel('F1 (Bark)', fontsize = 15)
    ax3.set_title("B", fontsize = 20)

    ax3.scatter(xb[:,1]
                , xb[:,0]
                , c=df_B_clean["nr_label"]
                , s = 10)

    ax3.set_ylim([1, 10])
    ax3.set_xlim([5, 14])
    ax3.grid()
    

    
    # for i, txt in enumerate(df_O_clean["label"]):
    #     ax1.annotate(txt, (xo[i,1], xo[i,0]))

    # for i, txt in enumerate(df_J_clean["label"]):
    #     ax2.annotate(txt, (xj[i,1], xj[i,0]))

    # for i, txt in enumerate(df_B_clean["label"]):
    #     ax3.annotate(txt, (xb[i,1], xb[i,0]))
    
    plt.gca().invert_yaxis()
    plt.gca().invert_xaxis()

    fig2 = plt.figure(None)
    plt.title("All three in one plot")
    plt.xlabel("F2 (Bark)")
    plt.ylabel("F1 (Bark)")
    po = plt.scatter(xo[:,1]
            , xo[:,0]
            #,c = df_O_clean["label"]
            ,s = 10)
    pj = plt.scatter(xj[:,1]
            , xj[:,0]
            #, c = df_J_clean["label"]
            , s = 10)
    pb = plt.scatter(xb[:,1]
            , xb[:,0]
            #, c = df_B_clean["label"]

            , s = 10)
    
    plt.legend((po, pj, pb), ("O", "J", "B"))
    plt.gca().invert_yaxis()
    plt.gca().invert_xaxis()

def plotCompare(model_b_to_j, model_b_to_o, df_B, df_J, df_O, sb, sj, so):
    X_B = df_B[["F1", "F2"]].values
    X_J = df_J[["F1", "F2"]].values
    X_O = df_O[["F1", "F2"]].values


    b_to_j_predicted_x = model_b_to_j.predict(X_B)
    b_to_o_predicted_x = model_b_to_o.predict(X_B)

    #Bark conversion
    b_to_j_predicted_x = (26.81*b_to_j_predicted_x)/(1960+b_to_j_predicted_x)-0.53
    b_to_o_predicted_x = (26.81*b_to_o_predicted_x)/(1960+b_to_o_predicted_x)-0.53

    X_J = (26.81*X_J)/(1960+X_J)-0.53
    X_O = (26.81*X_O)/(1960+X_O)-0.53





    print("Plotting data")
    fig1 = plt.figure(None)
    ax1 = fig1.add_subplot(1,2,1) 
    ax1.set_xlabel('F2 (Bark)', fontsize = 15)
    ax1.set_ylabel('F1 (Bark)', fontsize = 15)
    ax1.set_title(sb + " to " + sj, fontsize = 20)

    bj_p = ax1.scatter(b_to_j_predicted_x[:,1]
                , b_to_j_predicted_x[:,0]
                , c = 'r'
                , s = 10)

    j_p = ax1.scatter(X_J[:,1]
                , X_J[:,0]
                , c = 'b'
                , s = 10)
    ax1.grid()
    plt.gca().invert_yaxis()
    plt.gca().invert_xaxis()

    ax2 = fig1.add_subplot(1,2,2) 
    ax2.set_xlabel('F2', fontsize = 15)
    ax2.set_ylabel('F1', fontsize = 15)
    ax2.set_title(sb + " to " + so, fontsize = 20)

    bo_p = ax2.scatter(b_to_o_predicted_x[:,1]
                , b_to_o_predicted_x[:,0]
                , c = 'g'
                , s = 10)

    o_p = ax2.scatter(X_O[:,1]
                , X_O[:,0]
                , c = 'y'
                , s = 10)
    ax2.grid()
    plt.gca().invert_yaxis()
    plt.gca().invert_xaxis()
    
    plt.legend((bj_p, j_p, bo_p, o_p), (sb + "->" + sj, sj, sb + "->" +so, so))

def helmut_plot(df_B, df_J, df_O):
    df_B_clean = df_B[df_B["include"] == 1]
    df_J_clean = df_J[df_J["include"] == 1]
    df_O_clean = df_O[df_O["include"] == 1]

    df_B_clean = df_B_clean[df_B_clean["label"].isin(["A:", "i:", "o:", "u:", "e:"])]
    df_J_clean = df_J_clean[df_J_clean["label"].isin(["A:", "i:", "o:", "u:", "e:"])]
    df_O_clean = df_O_clean[df_O_clean["label"].isin(["A:", "i:", "o:", "u:", "e:"])]
    

    b = np.zeros(shape=(6,2))
    b[0] = [df_B_clean[df_B_clean["label"] == "i:"]["F1"].mean(), df_B_clean[df_B_clean["label"] == "i:"]["F2"].mean()]
    b[1] = [df_B_clean[df_B_clean["label"] == "u:"]["F1"].mean(), df_B_clean[df_B_clean["label"] == "u:"]["F2"].mean()]
    b[2] = [df_B_clean[df_B_clean["label"] == "o:"]["F1"].mean(), df_B_clean[df_B_clean["label"] == "o:"]["F2"].mean()]
    b[3] = [df_B_clean[df_B_clean["label"] == "A:"]["F1"].mean(), df_B_clean[df_B_clean["label"] == "A:"]["F2"].mean()]
    b[4] = [df_B_clean[df_B_clean["label"] == "e:"]["F1"].mean(), df_B_clean[df_B_clean["label"] == "e:"]["F2"].mean()]
    b[5] = b[0]

    o = np.zeros(shape=(6,2))
    
    o[0] = [df_O_clean[df_O_clean["label"] == "i:"]["F1"].mean(), df_O_clean[df_O_clean["label"] == "i:"]["F2"].mean()]
    o[1] = [df_O_clean[df_O_clean["label"] == "u:"]["F1"].mean(), df_O_clean[df_O_clean["label"] == "u:"]["F2"].mean()]
    o[2] = [df_O_clean[df_O_clean["label"] == "o:"]["F1"].mean(), df_O_clean[df_O_clean["label"] == "o:"]["F2"].mean()]
    o[3] = [df_O_clean[df_O_clean["label"] == "A:"]["F1"].mean(), df_O_clean[df_O_clean["label"] == "A:"]["F2"].mean()]
    o[4] = [df_O_clean[df_O_clean["label"] == "e:"]["F1"].mean(), df_O_clean[df_O_clean["label"] == "e:"]["F2"].mean()]
    o[5] = o[0]

    j = np.zeros(shape=(6,2))
    
    j[0] = [df_J_clean[df_J_clean["label"] == "i:"]["F1"].mean(), df_J_clean[df_J_clean["label"] == "i:"]["F2"].mean()]
    j[1] = [df_J_clean[df_J_clean["label"] == "u:"]["F1"].mean(), df_J_clean[df_J_clean["label"] == "u:"]["F2"].mean()]
    j[2] = [df_J_clean[df_J_clean["label"] == "o:"]["F1"].mean(), df_J_clean[df_J_clean["label"] == "o:"]["F2"].mean()]
    j[3] = [df_J_clean[df_J_clean["label"] == "A:"]["F1"].mean(), df_J_clean[df_J_clean["label"] == "A:"]["F2"].mean()]
    j[4] = [df_J_clean[df_J_clean["label"] == "e:"]["F1"].mean(), df_J_clean[df_J_clean["label"] == "e:"]["F2"].mean()]
    j[5] = j[0]

    #Bark conversion
    b = (26.81*b)/(1960+b)-0.53
    o = (26.81*o)/(1960+o)-0.53
    j = (26.81*j)/(1960+j)-0.53

    label = ["i", "u", "o", "a", "e"]
    fig = plt.figure(None)
    plt.title("Helmut")
    plt.xlabel("F2 (Bark)")
    plt.ylabel("F1 (Bark)")
    pb = plt.plot(b[:,1]
            , b[:,0]
            , 'ro-'
            ,label="B")

    for i, txt in enumerate(label):
        plt.annotate(txt, (b[i,1], b[i,0]))

    pj = plt.plot(j[:,1]
            , j[:,0]
            , 'bo-'
            ,label="J")
    for i, txt in enumerate(label):
        plt.annotate(txt, (j[i,1], j[i,0]))

    po = plt.plot(o[:,1]
            , o[:,0]
            , 'go-'
            ,label="O")
    for i, txt in enumerate(label):
        plt.annotate(txt, (o[i,1], o[i,0]))

    plt.gca().invert_yaxis()
    plt.gca().invert_xaxis()
    
    plt.legend()

def main():
    df = readData()
    i = 0
    unique_vowels = df['label'].unique()
    df["nr_label"] = df["label"]
    for vowel in unique_vowels:
       df['nr_label'] =  df['nr_label'].replace(vowel, i)
       i += 1

    print(df['nr_label'])


    #df.dropna(axis=1, how='any')
    
    # Sepparate the data sets
    df_B = df[df['speaker'] == "B"].reset_index()
    df_J = df[df['speaker'] == "J"].reset_index()
    df_O = df[df['speaker'] == "O"].reset_index()

    print("Size B without zeros", df_B[df_B["include"] != 0].shape)
    print("Size J without zeros", df_J[df_J["include"] != 0].shape)
    print("Size O without zeros", df_O[df_O["include"] != 0].shape)


    
    # Imput missing values for F2 with mean
    #imput(df_B)
    #imput(df_J)
    #imput(df_O)

    
    cluster(df_B, df_J, df_O)
    '''
    helmut_plot(df_B, df_J, df_O)

    print("\n\n#####################\nWith O as goal\n##################\n")
    print("Fitting O to O")
    model_o_to_o = model1(df_O, df_O)
    print("--------------------------\nFitting J to O")
    model_j_to_o = model1(df_J, df_O)
    print("--------------------------\nFitting B to O")
    model_b_to_o = model1(df_B, df_O)

    print("\n\n#####################\nWith J as goal\n##################\n")
    print("Fitting J to J")
    model_j_to_j = model1(df_J, df_J)
    print("--------------------------\nFitting O to J")
    model_o_to_j = model1(df_O, df_J)
    print("--------------------------\nFitting B to J")
    model_b_to_j = model1(df_B, df_J)

    print("\n\n#####################\nWith B as goal\n##################\n")
    print("Fitting B to B")
    model_b_to_b = model1(df_B, df_B)
    print("--------------------------\nFitting J to B")
    model_j_to_b = model1(df_J, df_B)
    print("--------------------------\nFitting O to B")
    model_o_to_b = model1(df_O, df_B)

    plotCompare(model_b_to_j, model_b_to_o, df_B, df_J, df_O, 'B', 'J', 'O')
    #plotCompare(model_o_to_j, model_o_to_b, df_O, df_J, df_B)
    #saveDFs(df_B, df_J, df_O)
    '''
    plt.show()

main()
