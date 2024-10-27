#include <bits/stdc++.h>

using namespace std;
int numNodes = 0;
vector<bool> visited;
vector<bool> recStack;
vector<int> parent;

vector<vector<int>> graph;

bool isCyclicGraph(int v, vector<bool> &visited, vector<bool> &recStack, vector<int> &parent)
{
    if (!visited[v])
    {
        visited[v] = true;
        recStack[v] = true;

        for (int i = 0; i < numNodes; i++)
        {
            if (graph[v][i])
            {
                if (!visited[i] && isCyclicGraph(i, visited, recStack, parent))
                {
                    parent[i] = v;
                    return true;
                }
                else if (recStack[i])
                {
                    parent[i] = v;
                    return true;
                }
            }
        }
    }
    recStack[v] = false;
    return false;
}

void printCycle(int start, int end, vector<int> &parent)
{
    vector<int> cycle;
    cycle.push_back(end);
    for (int v = start; v != end; v = parent[v])
    {
        cycle.push_back(v);
    }
    cycle.push_back(end);
    reverse(cycle.begin(), cycle.end());

    cout << "Cycle found: ";
    for (int v : cycle)
    {
        cout << "T" << v + 1 << " ";
    }
    cout << "\n";
}

int main()
{
    vector<vector<string>> array;
    string line;
    ifstream inputFile("input.txt");

    if (!inputFile.is_open())
    {
        cerr << "Error opening file 'input.txt'\n";
        return 1;
    }

    while (getline(inputFile, line))
    {
        vector<string> row;
        stringstream ss(line);
        string value;
        while (getline(ss, value, ','))
        {
            row.push_back(value);
        }
        array.push_back(row);
    }

    inputFile.close();

    numNodes = array.size();
    graph.resize(numNodes, vector<int>(numNodes, 0));
    visited.resize(numNodes, false);
    recStack.resize(numNodes, false);
    parent.resize(numNodes, -1);

    for (int i = 0; i < numNodes; i++)
    {
        for (int j = 0; j < numNodes; j++)
        {
            graph[i][j] = 0;
        }
    }
    vector<pair<string, string>> transactions;
    for (int j = 0; j < array[0].size(); j++)
    {
        for (int i = 0; i < array.size(); i++)
        {
            if (array[i][j] != "-" && j != 0)
            {
                transactions.push_back({array[i][0], array[i][j]});
            }
        }
    }

    // for (int i = 0; i < transactions.size(); i++)
    // {
    //     if (transactions[i].second.substr(0, 1) == "W")
    //     {
    //         for (int j = 0; j < i; j++)
    //         {
    //             if (transactions[j].second[2] == transactions[i].second[2] && transactions[i].first[1] != transactions[j].first[1])
    //             {
    //                 graph[stoi(transactions[j].first.substr(1)) - 1][stoi(transactions[i].first.substr(1)) - 1] = 1;
    //             }
    //         }
    //     }
    // }
    
    for (int i = 0; i < transactions.size(); i++)
    {
        if (transactions[i].second.substr(0, 1) == "W")
        {
            for (int j = i; j < transactions.size(); j++)
            {
                if (transactions[j].second[2] == transactions[i].second[2] && transactions[i].first[1] != transactions[j].first[1])
                {
                    graph[stoi(transactions[i].first.substr(1)) - 1][stoi(transactions[j].first.substr(1)) - 1] = 1;
                }

            }
        }
        else if (transactions[i].second.substr(0, 1) == "R")
        {
            for (int j = i; j < transactions.size(); j++)
            {
                if (transactions[j].second[2] == transactions[i].second[2] && transactions[i].first[1] != transactions[j].first[1] && transactions[j].second.substr(0, 1) == "W")
                {
                    graph[stoi(transactions[i].first.substr(1)) - 1][stoi(transactions[j].first.substr(1)) - 1] = 1;
                }
            }
        }
    }
    cout << "Graph adjacency matrix:\n";
    for (int i = 0; i < numNodes; i++)
    {
        for (int j = 0; j < numNodes; j++)
        {
            cout << graph[i][j] << " ";
        }
        cout << "\n";
    }

    bool isCyclic = false;
    for (int i = 0; i < numNodes; i++)
    {
        if (isCyclicGraph(i, visited, recStack, parent))
        {
            isCyclic = true;
            printCycle(i, parent[i], parent);
            break;
        }
    }

    if (!isCyclic)
        cout << "Graph doesn't contain a cycle\n";

    return 0;
}
