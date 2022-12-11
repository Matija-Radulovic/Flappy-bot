import random
import numpy as np
import math
import copy     #!bias... add as column?

class Network:#classes for clarity or matrices for speed?
                #bias and weights ????
                #?
    
    def __init__(self,input_size,hidden_size,output_size,hid_layer_num):
        self.input_size=input_size
        self.hidden_size=hidden_size
        self.output_size=output_size
        self.hid_layer_num=hid_layer_num    

        
        self.weights=[]    #hmmm
        
        
        self.biases=[]   

        #random, input normalization etc...?
        
        
        self.weights[0] = np.zeros((self.input_size, self.hidden_size))

        for n in range(1,hid_layer_num):
            self.hidden_weights[n] = np.zeros(self.hidden_size, self.hidden_size)

        self.weights[hid_layer_num] = np.zeros(self.hidden_size, self.output_size)

        
        
        
        for n in range(hid_layer_num):
            self.hidden_biases[n] = np.zeros(self.hidden_size)        
        self.biases[hid_layer_num] = np.zeros(self.output_size)
        
        
    

    def SetValues(self,layer,from_node,to_node,weight,bias):
        pass
    def MutantClone(self, prob, amount):
        clone=copy.deepcopy(self)

        for n in range(1,self.hid_layer_num+2):

            (layer_weights,layer_biases)=self.get_values_for_layer(n)
            
            num_weights=len(layer_weights)
            num_nodes=len(layer_biases)
            
            for i in range(num_nodes):
                if random.random()<prob:
                    layer_biases[i]+= random.gauss(0,amount)
        
                for j in range(num_weights):
                    if random.random()<prob:#full mutate?
                        layer_weights[i,j]+= random.gauss(0,amount)
                        
                
        return clone
    
    @staticmethod
    def MakeChild(parent1,parent2,cross_prob=0): 
        clone= copy.deepcopy(parent1)
        
        for n in range(1,parent1.hid_layer_num+2):

            (layer_weights1,layer_biases1)=parent1.get_values_for_layer(n)
            (layer_weights2,layer_biases2)=parent2.get_values_for_layer(n)
            (layer_weightsc,layer_biasesc)=clone.get_values_for_layer(n)
            
            num_weights=len(layer_weights1)
            num_nodes=len(layer_biases1)
            
            for i in range(num_nodes):
                if random.random()<cross_prob:#?
                    layer_biasesc[i]= (layer_biases1[i]+layer_biases2[i])/2
                else:
                    if random.random<0.5:
                        layer_biasesc[i]=layer_biases1[i]
                    else:
                        layer_biasesc[i]=layer_biases2[i]

                for j in range(num_weights):
                    if random.random()<cross_prob:
                        layer_weightsc[i,j]= (layer_weights1[i,j]+layer_weights2[i,j])/2
                    else:
                        if(random.random<0.5):
                            layer_weightsc[i,j]=layer_weights1[i,j]
                        else:
                            layer_weightsc[i,j]=layer_weights2[i,j]

        return clone

    @staticmethod
    
    def __Sigmoid(x): #static, here?, activation? 
        return 1/(1 + np.exp(-x))
        pass

     
    def get_values_for_layer(self,layer):
        return (self.weights[layer-1],self.hidden_biases[layer-1])
    
    
    
    
    def get_values_for_node(self,layer,node): 
        (layer_wights,layer_biases)=self.get_values_for_layer(layer)
        return (layer_wights[:,node],layer_biases[node])
    
    def NodeCalculateOutput(self,layer,node,inputs):
        weights,bias=self.get_values_for_node(layer,node)
        return np.dot(inputs,weights)+bias   
    def NodeOutput(self,layer,node,inputs):
        x=self.NodeCalculateOutput(layer,node,inputs)
        return Network.__Sigmoid(x)



    
    @staticmethod        
    def __LayerOutputs(inputs, weights, biases):
        return Network.__Sigmoid( np.dot(inputs,weights)+biases) #?

    def Output(self,inputs):
        #for n in range
        curr_layer_out= inputs
        
        for i in range(1,self.hid_layer_num+2):
            (weights,biases)=self.get_values_for_layer(i)
            curr_layer_out= Network.__LayerOutputs(curr_layer_out,weights,biases)

        return curr_layer_out

    #separate agent with game network fitnes etc?
    def print(self):
        ret=''
        for i in range(self.hidden_size+1):
            b = '\n'.join('\t'.join('%0.3f' %x for x in y) for y in self.weights[i])
            c= ('\t'.join('%0.3f' %y) for y in self.biases[i])
            ret+=b+'\n'+c+'\n'
        return 