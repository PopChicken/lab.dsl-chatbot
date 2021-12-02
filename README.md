# Customer Service Bot Based on Django and Vue

[example webapp](https://chatbot.lab.jnn.icu)

A final project of Program Designing course in Beijing University of Posts and Telecommunications.

## Brief

This application defined a DSL (Domain Specific Languages), which can describe the behavior of a customer service bot.

The defination file of the bot in the [example webapp](https://chatbot.lab.jnn.icu):

```
service "理财"
    text "产品介绍" "A产品：中风险...; B产品：低风险; C产品：高风险"
    script "理财产品推荐评估" "evaluate"
    faq "常见问题"
        "我适合什么样的理财产品？": "选择理财产品需要根据自己对风险的承受能力，可以问我“理财产品推荐评估”进行评估。"
        "七日年化利率与年利率有什么区别？": "七日年化利率是通过过去七日的收益情况估计的年利率，未来具有不确定性；而年利率是固定的，没有不确定性。"
        "如何使用定期投资功能？": "前往首页，在金融功能栏下可以看到定期投资功能。"

service "基础金融业务"
    text "产品介绍" "手机银行APP可以使用转账、查询、账户管理、新卡申请、新卡激活、银行卡管理等功能"
    script "附近网点查询" "querybranch"

```

This defination file shows the struction of the DSL and some grammar rules.

Like Python, my DSL uses indentation to define a code block. The defination file will be loaded by the backend.

If the backend parsed it successfully, an automaton will be built with several data node indexed by its transition table.

### DSL defination

#### Root

This is a hidden declaration, represented by the declaration set with lowest level of indentation.

**service** is the only declaration allowed in **root.**

#### Service

`service "<name of service>"`

**service** declaration povides recursive definations.

Declaring a **service** under a **root** or another **service** means to create a subservice under it. Users can enter it or exit it.

The `name of service` will be showed in the welcoming message when a user enters it.

The string behind it is its name. Send this string to the bot will enter this subservice.

The default word to exit is `返回`, which can be modified in `bot.py`. A welcoming message (of father) will be also showed when a user exit to the father service.

#### Text

`text "<name of option>" "<answer>"`

This is a basic QA but unlike FAQ. It will be showed as an option in the welcoming message.

#### Script

`script "<name of option>" ["<tips to type arguments>"] "<script to execute>"`

This declaration provides a powerful tool to customize your bot.

You can execute any Python script with it.

When user selects the script option (`<tips to type arguments>` not added), the bot will execute the `handle` funtion defined under your module `<script to execute>` then reply the string it returned.

If you added the optional argument `<tips to type arguments>`, the bot will wait for one `message` as the argument to call the function `handle(message)`.

`<tips to type arguments>` is sent to user before he types the arguments in order to show the explanation of arguments.

#### FAQ

`faq "<name of option to show all QAs in the FAQ>"`

Any questions not captured by other options will be searched in QAs in the FAQ.

User can also select FAQ option to get all things in the FAQ sub-block.

#### FAQItem

`"<question>": "<answer>"`

The declaration of items in the sub-block of FAQ declaration.
