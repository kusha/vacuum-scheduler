<!-- <a name="readme-top"></a> -->

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <!-- <a href="https://github.com/kusha/vacuum-scheduler">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

  <h3 align="center">vacuum-scheduler</h3>

  <p align="center">
    A powerful AppDaemon app for scheduling vacuum cleaner operations in Home Assistant.
    <!-- <br />
    <a href="https://github.com/kusha/vacuum-scheduler"><strong>Explore the docs »</strong></a>
    <br /> -->
    <br />
    **It is still a little buggy as I've just starting using it myself. Give it a star and come back in couple weeks!**
    <br />
    <!-- <a href="https://github.com/kusha/vacuum-scheduler">View Demo</a>
    · -->
    <a href="https://github.com/kusha/vacuum-scheduler/issues">Report Bug</a>
    ·
    <a href="https://github.com/kusha/vacuum-scheduler/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <!-- <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul> -->
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

Autonomous vacuum cleaners are one of the best inventions of humanity, which saves a lot of time. I love clean floors, but I really dislike listening to the noise of a vacuum cleaner. Setting a cleaning schedule for a specific time in a certain area just doesn't work because often you are in that room or sleeping at that time. The goal of this automation is to maximize the time when the vacuum cleaner works when there is nobody at home. Although, there are days when you work from home and stay there longer than the desired cleaning time, but you still want the floor to remain clean. This automation allows you to solve this problem by flexible interval settings and planning for the next cleanings.

### Features

- Configuring independent cleaning of multiple rooms (zones or automatically detected segments).
- Agnostic of the vacuum model, as it uses standard Home Assistant service calls.
- Setting different desired cleaning frequencies for each room or zone.
- Using a sensor that detects the absence of people at home.
- Setting coefficient to define when the robot will start cleaning, even if there are people at home (when cleaning has not been done for a long time).
- Setting coefficient to define the minimum time after which a room should be cleaned if no one is home (clean rooms that should be cleaned soon while home is empty). 

<!-- ### Built With

* [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]
* [![Angular][Angular.io]][Angular-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Laravel][Laravel.com]][Laravel-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url] -->

<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

Home Assistant with AppDaemon addon installed. HACS installed.

### Installation

TODO
<!-- 1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/kusha/vacuum-scheduler.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ``` -->

<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- USAGE EXAMPLES -->
## Usage

TODO

<!-- _For more examples, please refer to the [Documentation](https://example.com)_ -->

<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- ROADMAP -->
## Roadmap

- [ ] Pause cleaning if the residents of the apartment return home.
- [ ] Schedule using CronTab syntax instead of a set of time slots.
- [ ] Customizable coefficients (see description).
- [ ] Support system calls for standard vacuum firmware such as Valetudo and Valetudo-RE.
- [ ] Optimization of scheduling to reduce the number of `run_at` AppDaemon calls.
- [ ] Notify about cleaning to mobile phone.
- [ ] Ability to postpone cleaning directly from the mobile phone notification.
- [ ] Automatic adjustment of suction power based on the presence of people at home.
- [ ] Enhanced monitoring of interrupted cleaning (manually or due to an error) through tracking of the cleaned area.
- [ ] Sorting of rooms scheduled at the same time based on the last cleaning.
- [ ] Extensive configuration options for static parameters.
- [ ] Automation blueprint to react on postpone from mobile notifications.


See the [open issues](https://github.com/kusha/vacuum-scheduler/issues) for a full list of proposed features (and known issues).

<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- CONTACT -->
<!-- ## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

Project Link: [https://github.com/kusha/vacuum-scheduler](https://github.com/kusha/vacuum-scheduler) -->

<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- ACKNOWLEDGMENTS -->
<!-- ## Acknowledgments

* []()
* []()
* []() -->

<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/kusha/vacuum-scheduler.svg?style=for-the-badge
[contributors-url]: https://github.com/kusha/vacuum-scheduler/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/kusha/vacuum-scheduler.svg?style=for-the-badge
[forks-url]: https://github.com/kusha/vacuum-scheduler/network/members
[stars-shield]: https://img.shields.io/github/stars/kusha/vacuum-scheduler.svg?style=for-the-badge
[stars-url]: https://github.com/kusha/vacuum-scheduler/stargazers
[issues-shield]: https://img.shields.io/github/issues/kusha/vacuum-scheduler.svg?style=for-the-badge
[issues-url]: https://github.com/kusha/vacuum-scheduler/issues
[license-shield]: https://img.shields.io/github/license/kusha/vacuum-scheduler.svg?style=for-the-badge
[license-url]: https://github.com/kusha/vacuum-scheduler/blob/master/LICENSE.txt
<!-- [linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username -->
<!-- [product-screenshot]: images/screenshot.png -->
