![Python application](https://github.com/Vasiliy566/NERPA/workflows/Python%20application/badge.svg)
# NERPA
1. Reformat antismash5 output to antismash3 format
2. Predict NRPS by 10-aa code
3. Improve Nrpsp_redictor algorithm

## Getting Started

```
git clone https://github.com/Vasiliy566/NERPA.git
```

### Prerequisites

Requirements in requirements.txt file

install with following command:
```
pip3 install -r requirements.txt
```


## Running the tests

to run test go to tests fiolder:
```
cd tests
```
and ryn pytest:
```
pytest .
```
### Break down into end to end tests

There are two tests:
test Piplines tests/Piplines_test.py
and test Dictionary handler -> tests/Dictionary_handler.py


### And coding style tests

Testt code style according to flake8

if not flake8 installed 
```
pip install flake8 
```
then run folowwing command in main repo
```
flake8
```

## Built With

* [Pytohn3](https://www.python.org/)

## Versioning

For the versions available, see the [tags on this repository](https://github.com/Vasiliy566/NERPA/tags). 

## Authors

* **Isaev Vasily** - *Coding* - [Vasiliy566](https://github.com/Vasiliy566)

* **Gurevich Alexey** - *scientific director* - [Gurevich Alexey](http://bioinformaticsinstitute.ru/teachers/gurevich)

* **Ol'ga kunyavskaya** - *scientific director*

See also the list of [contributors](https://github.com/Vasiliy566/NERPA/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
