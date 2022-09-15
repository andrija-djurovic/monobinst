# monobinst

The purpose of this application is to create Streamlit UI for [monobinpy](https://pypi.org/project/monobinpy) package.
For time being application can be run only locally, and the main requirements are given below:
```cmd
streamlit
pandas
monobinpy
pathlib
base64
os
inspect
st_aggrid
PIL

``` 

Using ```git clone``` user can easily set up the application environment following the next 3 steps:

*   Step 1 - open cmd and set working directory:
```cmd
cd "your application directory" 

```
*   Step 2 - clone the repository using ```git clone```:
```cmd
git clone https://github.com/andrija-djurovic/monobinst

```
*   Step 3 - move working directory for one folder up and start app using ```streamlit```:
```cmd
cd ".monobinst"
streamlit run app.py

```

Another way to set up the application enviornment is to download repository zip file, then to unzipp it in selected folder
and finally to run ```streamlit``` from the same folder (like the 3rd step from above). 

Happy Streamlit-ing 😄
