## AWS CloudFormation

### Template ([JSON/YAML](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html?shortFooter=true))

* You must ensure that all dependent resources that the template requires are available.
* A template can use or refer to both existing AWS resources and resources declared in the template itself.
* 6 Top Level Objects
  * AWSTemplateFormatVersion
  * Description
  * Parameters
    * Effective way of sepcifying sensitive information
    * Receives user inputs
  * Mappings
    * Conditional values that are evaluated in a similar manner as a _switch_ statement
  * Outputs
    * Defines value return by `cfn-describe-stacks`
  * **_Resources(Required)_**
    * start with logical name of the AWS resource
    * The `Type` attribute has s [special format](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html?shortFooter=true):
    ```
    AWS::ProductIdentifier::ResourceType
    ```
    * [Ref function](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html?shortFooter=true): setup resource properties from the value of another _resource_(can be literal name of an existing resources i.e., security groups, key name) or _parameter_
    * [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html?shortFooter=true) function: get addtional attributes value of target resource
    * For full list of resource types, see **[Template References](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-reference.html?shortFooter=true)**

