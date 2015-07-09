#include "subtree.h"
#include "morrf.h"

RRTNode::RRTNode(POS2D pos, int objective_num)
{
    mPos = pos;
    mObjectiveNum = objective_num;

    mpCost = new double[mObjectiveNum];
    mFitness = 0.0;
    mpParent = NULL;
}

bool RRTNode::operator==(const RRTNode &other)
{
    return mPos==other.mPos;
}

RRTree::RRTree(MORRF* parent, int objective_num, double * p_weight)
{
    mpParent = parent;
    mType = REFERENCE;
    mObjectiveNum = objective_num;
    mIndex = -1;
    mpWeight = new double[mObjectiveNum];
    if(p_weight)
    {
        for(int k=0;k<mObjectiveNum;k++)
        {
            mpWeight[k] = p_weight[k];
        }
    }

    mpRoot = NULL;
    mNodes.clear();
}

RRTNode* RRTree::init(POS2D start, POS2D goal)
{
    if(mpRoot)
    {
        delete mpRoot;
        mpRoot = NULL;
    }
    mStart = start;
    mGoal = goal;
    mpRoot = new RRTNode(start, mObjectiveNum);
    mNodes.push_back(mpRoot);

    return mpRoot;
}

RRTNode*  RRTree::createNewNode(POS2D pos)
{
    RRTNode * pNode = new RRTNode(pos, mObjectiveNum);
    mNodes.push_back(pNode);

    return pNode;
}

bool RRTree::removeEdge(RRTNode* pNode_p, RRTNode*  pNode_c)
{
    if(pNode_p==NULL)
    {
        return false;
    }

    pNode_c->mpParent = NULL;
    bool removed = false;
    for(std::list<RRTNode*>::iterator it=pNode_p->mChildNodes.begin();it!=pNode_p->mChildNodes.end();it++)
    {
        RRTNode* pCurrent = (RRTNode*)(*it);
        if (pCurrent==pNode_c)
        {
            pCurrent->mpParent = NULL;
            it = pNode_p->mChildNodes.erase(it);
            removed = true;
        }
    }
    return removed;
}

bool RRTree::hasEdge(RRTNode* pNode_p, RRTNode* pNode_c)
{
    if (pNode_p==NULL || pNode_c==NULL)
        return false;
    if (pNode_p == pNode_c->mpParent)
        return true;
    return false;
}

bool RRTree::addEdge(RRTNode* pNode_p, RRTNode* pNode_c)
{
    if (pNode_p == pNode_c)
    {
        return false;
    }
    if (hasEdge(pNode_p, pNode_c))
    {
        pNode_c->mpParent = pNode_p;
    }

    pNode_p->mChildNodes.push_back(pNode_c);
    pNode_c->mpParent = pNode_p;

    return true;
}


std::list<RRTNode*> RRTree::findAllChildren(RRTNode* pNode)
{
    int level = 0;
    bool finished = false;
    std::list<RRTNode*> child_list;

    std::list<RRTNode*> current_level_nodes;
    current_level_nodes.push_back(pNode);
    while(false==finished)
    {
        std::list<RRTNode*> current_level_children;
        int child_list_num = current_level_children.size();

        for(std::list<RRTNode*>::iterator it=current_level_nodes.begin(); it!=current_level_nodes.end(); it++)
        {
            RRTNode* pCurrentNode = (*it);
            for(std::list<RRTNode*>::iterator itc=pCurrentNode->mChildNodes.begin(); itc!=pCurrentNode->mChildNodes.end();itc++)
            {
                RRTNode *pChildNode= (*itc);
                current_level_children.push_back(pChildNode);
                child_list.push_back(pChildNode);
            }

        }

        if (current_level_children.size()==0)
            finished = true;
        else if (child_list.size()==child_list_num)
        {
            finished = true;
        }
        else
        {
            current_level_nodes = current_level_children;
            level +=1;
        }
    }

    return child_list;
}

ReferenceTree::ReferenceTree(MORRF* parent, int objective_num, int index)
    : RRTree(parent, objective_num, NULL)
{
    mIndex = index;
}

ReferenceTree::~ReferenceTree()
{

}

void ReferenceTree::attachNewNode(RRTNode* pNode_new, KDNode2D node_nearest, std::list<KDNode2D> near_nodes)
{
    RRTNode* pNearestNode = node_nearest.mNodeList[mIndex];
    double min_new_node_fitness = pNearestNode->mFitness + mpParent->calcCost(pNearestNode->mPos, pNode_new->mPos, mIndex);
    RRTNode* pMinNode = pNearestNode;

    for(std::list<KDNode2D>::iterator it=near_nodes.begin();it!=near_nodes.end();it++)
    {
        RRTNode* pNearNode = it->mNodeList[mIndex];
        if (true == mpParent->isObstacleFree(pNearNode->mPos, pNode_new->mPos))
        {
            double fitness = pNearNode->mFitness + mpParent->calcCost(pNearNode->mPos, pNode_new->mPos, mIndex);
            if (fitness < min_new_node_fitness)
            {
                pMinNode = pNearNode;
                min_new_node_fitness = fitness;
            }
        }
    }

    addEdge(pMinNode, pNode_new);
    pNode_new->mFitness = min_new_node_fitness;

}

void ReferenceTree::rewireNearNodes(RRTNode* pNode_new, std::list<KDNode2D> near_nodes)
{
    for(std::list<KDNode2D>::iterator it=near_nodes.begin(); it!=near_nodes.end(); it++)
    {
        KDNode2D near_node = (KDNode2D)(*it);

        RRTNode * pNearNode = near_node.mNodeList[mIndex];

        if(pNearNode->mPos ==pNode_new->mPos ||  pNearNode->mPos==mpRoot->mPos || pNode_new->mpParent->mPos==pNearNode->mPos)
        {
            continue;
        }

        if(true==mpParent->isObstacleFree(pNode_new->mPos, near_node))
        {
            double temp_fitness_from_new_node = pNode_new->mFitness + mpParent->calcCost(pNode_new->mPos, pNearNode->mPos, mIndex);
            if(temp_fitness_from_new_node < pNearNode->mFitness)
            {
                RRTNode * pParentNode = pNearNode->mpParent;
                removeEdge(pParentNode, pNearNode);
                addEdge(pNode_new, pNearNode);

                double delta_fitness = pNearNode->mFitness - temp_fitness_from_new_node;
                updateFitnessToChildren(pNearNode, delta_fitness);
            }
        }

    }
}

void ReferenceTree::updateFitnessToChildren(RRTNode* pNode, double delta_fitness)
{
    std::list<RRTNode*> child_list = findAllChildren(pNode);
    for(std::list<RRTNode*>::iterator it=child_list.begin();it!=child_list.end();it++)
    {
        RRTNode* pChildNode = (*it);
        if(pChildNode)
        {
            pChildNode->mFitness -= delta_fitness;
        }
    }

}

SubproblemTree::SubproblemTree(MORRF* parent, int objective_num, double * p_weight, int index)
    : RRTree(parent, objective_num, p_weight)
{
    mIndex = index;
}

SubproblemTree::~SubproblemTree()
{

}


void SubproblemTree::attachNewNode(RRTNode* pNode_new, KDNode2D node_nearest, std::list<KDNode2D> near_nodes)
{
    RRTNode* pNearestNode = node_nearest.mNodeList[mIndex];
    double p_min_new_node_cost[mObjectiveNum];
    double p_min_new_node_cost_delta[mObjectiveNum];
    mpParent->calcCost(pNearestNode->mPos, pNode_new->mPos, p_min_new_node_cost_delta);
    for(int k=0;k<mObjectiveNum;k++)
    {
        p_min_new_node_cost[k] = pNearestNode->mpCost[k] + p_min_new_node_cost_delta[k];
    }
    double min_new_node_fitness = mpParent->calcFitness(p_min_new_node_cost, mpWeight, pNode_new->mPos);

    RRTNode* pMinNode = pNearestNode;

    for(std::list<KDNode2D>::iterator it=near_nodes.begin();it!=near_nodes.end();it++)
    {
        RRTNode* pNearNode = it->mNodeList[mIndex];
        if (true == mpParent->isObstacleFree(pNearNode->mPos, pNode_new->mPos))
        {
            double p_cost_temp[mObjectiveNum];
            double p_cost_delta[mObjectiveNum];
            mpParent->calcCost(pNearNode->mPos, pNode_new->mPos, p_cost_delta);
            for(int k=0;k<mObjectiveNum;k++)
            {
                p_cost_temp[k] = pNearNode->mpCost[k] + p_cost_delta[k];
            }
            double fitness = mpParent->calcFitness(p_cost_temp, mpWeight, pNode_new->mPos);
            if (fitness < min_new_node_fitness)
            {
                pMinNode = pNearNode;
                min_new_node_fitness = fitness;
                for(int k=0;k<mObjectiveNum;k++)
                {
                    p_min_new_node_cost[k] = p_cost_temp[k];
                }
            }
        }
    }

    addEdge(pMinNode, pNode_new);
    pNode_new->mFitness = min_new_node_fitness;
    for(int k=0;k<mObjectiveNum;k++)
    {
       pNode_new->mpCost[k] = p_min_new_node_cost[k];
    }
}

void SubproblemTree::rewireNearNodes(RRTNode* pNode_new, std::list<KDNode2D> near_nodes)
{
    for(std::list<KDNode2D>::iterator it=near_nodes.begin(); it!=near_nodes.end(); it++)
    {
        KDNode2D near_node = (KDNode2D)(*it);

        RRTNode * pNearNode = near_node.mNodeList[mIndex+mObjectiveNum];

        if(pNearNode->mPos == pNode_new->mPos ||  pNearNode->mPos == mpRoot->mPos || pNode_new->mpParent->mPos == pNearNode->mPos)
        {
            continue;
        }

        if(true==mpParent->isObstacleFree(pNode_new->mPos, near_node))
        {
            double temp_cost_from_new_node[mObjectiveNum];
            double temp_delta_cost_from_new_node[mObjectiveNum];

            mpParent->calcCost(pNode_new->mPos, pNearNode->mPos, temp_delta_cost_from_new_node);
            for(int k=0;k<mObjectiveNum;k++)
            {
                temp_cost_from_new_node[k] = pNode_new->mpCost[k] + temp_delta_cost_from_new_node[k];
            }
            double temp_fitness_from_new_node = mpParent->calcFitness(temp_cost_from_new_node, mpWeight, pNearNode->mPos);

            if(temp_fitness_from_new_node < pNearNode->mFitness)
            {
                RRTNode * pParentNode = pNearNode->mpParent;
                removeEdge(pParentNode, pNearNode);
                addEdge(pNode_new, pNearNode);
                double delta_cost[mObjectiveNum];
                for(int k=0;k<mObjectiveNum;k++)
                {
                    delta_cost[k] = pNearNode->mpCost[k] - temp_cost_from_new_node[k];
                    pNearNode->mpCost[k] = temp_cost_from_new_node[k];
                    pNearNode->mFitness = temp_fitness_from_new_node;
                }
                updateCostToChildren(pNearNode, delta_cost);
            }
        }

    }

}

void SubproblemTree::updateCostToChildren(RRTNode* pNode, double* pDelta_cost)
{
    std::list<RRTNode*> child_list = findAllChildren(pNode);
    for(std::list<RRTNode*>::iterator it=child_list.begin();it!=child_list.end();it++)
    {
        RRTNode* pChildNode = (*it);
        if(pChildNode)
        {
            for(int k=0;k<mObjectiveNum;k++)
            {
                pChildNode->mpCost[k] -= pDelta_cost[k];
            }
            pChildNode->mFitness = mpParent->calcFitness(pChildNode->mpCost, mpWeight, pChildNode->mPos);
        }
    }
}

