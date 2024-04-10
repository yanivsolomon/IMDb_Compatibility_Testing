Compatibility Testing for IMDb.com

This compatibility testing was created using Python, Selenium WebDriver, and the Pytest framework. It encompasses the following tests:

Screen Resolution Compatibility:
Validates size and visibility for the following elements on a default 13-inch laptop:
Logo
Menu
Headline
Repeats the tests after changing the viewport to different sizes (S, M, L phones, and an average tablet).
Language Compatibility:
Verifies that the website correctly supports different languages. The following elements are tested in English, French, and German:
Headline text
Menu text
Searchbar placeholder text.
Browser Compatibility:
Repeats the Screen Resolution test (originally done on Edge) on Firefox and Chrome.
