car-data-scraper
================

Take the carData.csv file and delete all of the crap you're not interested in. Then 

    `python carData.py cardata.csv output.json`
    
You'll need to come up with a way to crunch down the json data on your own.

Example
-------

```
{
   "Jeep / Compass / 2011": {
      "pricing": {
         "sport-suv-4d": {
            "cpo": {
               "priceMin": 16113.0,
               "price": 16969.0,
               "priceMax": 17824.0
            },
            "retail": {
               "priceMin": 0.0,
               "price": 16319.0,
               "priceMax": 0.0
            },
            "privatepartyexcellent": {
               "priceMin": 0.0,
               "price": 14840.0,
               "priceMax": 0.0
            },
            "privatepartyverygood": {
               "priceMin": 0.0,
               "price": 14351.0,
               "priceMax": 0.0
            },
            "privatepartygood": {
               "priceMin": 0.0,
               "price": 13917.0,
               "priceMax": 0.0
            },
            "privatepartyfair": {
               "priceMin": 0.0,
               "price": 12706.0,
               "priceMax": 0.0
            },
            "fpp": {
               "priceMin": 13849.0,
               "price": 15469.0,
               "priceMax": 17088.0
            }
         },
         "limited-sport-utility-4d": {
            "cpo": {
               "priceMin": 18245.0,
               "price": 19176.0,
               "priceMax": 20106.0
            },
            "retail": {
               "priceMin": 0.0,
               "price": 18526.0,
               "priceMax": 0.0
            },
            "privatepartyexcellent": {
               "priceMin": 0.0,
               "price": 16919.0,
               "priceMax": 0.0
            },
            "privatepartyverygood": {
               "priceMin": 0.0,
               "price": 16405.0,
               "priceMax": 0.0
            },
            "privatepartygood": {
               "priceMin": 0.0,
               "price": 15933.0,
               "priceMax": 0.0
            },
            "privatepartyfair": {
               "priceMin": 0.0,
               "price": 14633.0,
               "priceMax": 0.0
            },
            "fpp": {
               "priceMin": 15817.0,
               "price": 17576.0,
               "priceMax": 19334.0
            }
         }
      },
      "ratings": {
         "Owner-Reported Fuel Economy": 3.0,
         "mpgCity": 21.0,
         "Body & Interior Quality - Design": 4.0,
         "Body & Interior Quality - Mechanical": 3.0,
         "Overall Dependability": 4.0,
         "Overall Quality - Design": 5.0,
         "Features & Accessories Quality - Design": 4.0,
         "mpgHwy": 26.0,
         "Powertrain Quality - Mechanical": 3.0,
         "Body and Interior Dependability": 4.0,
         "Style": 3.0,
         "Powertrain Dependability": 3.0,
         "Comfort": 3.0,
         "Overall Quality": 4.0,
         "Powertrain Quality - Design": 4.0,
         "Feature and Accessory Dependability": 4.0,
         "Features and Instrument Panel": 3.0,
         "Performance": 3.0,
         "Features & Accessories Quality - Mechanical": 4.0,
         "Overall Performance and Design": 3.0,
         "Overall Quality - Mechanical": 3.0
      }
   }
}

```

