# Frequently Asked Questions

Hopefully we can answer all of your questions here if there is no relevant place in other documents.
Please do contribute additional questions you would like answered.

## Why did you ...

* **... name this "Syntrend"?**

  **Syntrend** is a portmonteau of "Synthetic" and "Trend" ("Syn-Trend") to emphasize the idea of a Synthetic generator based on a trend using expressions. Other names considered were:

  * "Syntropy": ("Synthetic" and "Entropy") to emphasize the Synthetic nature of data generation with variability/chaos.

* **... not use JSONSchema?**

  The original intent was to use JSONSchema as many data sources being synthesized would have a matching JSONSchema, but this raised a number of challenges:

  1. There would need to be a way to define patterns for the data to exhibit in a JSONSchema format.
  2. Supporting the many versions of JSONSchema and the poor compatibility that goes with it added additional complexity. Also considered creating a dedicated project to parse JSONSchema to generate data saw little value in the developer environment.
  3. Assumes all data sources have a JSONSchema available.

* **... not use JSON?**

  This would be easy to implement but thinking about the target audience and how the project files would be maintained, readability and repeatability was a main concern. JSON struggles with these as it's primarily an exchange format.

  YAML has the benefit of being highly human-readable with native support for anchors to re-use portions across multiple locations in a project.
