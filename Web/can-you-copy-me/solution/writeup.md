# 解题思路

## 工具

不需要啥特别的工具。

## 步骤

本题实际上分两部分，第一部分是通过 CSS 和 JS 实现（大部分反复制都是这么干的）反复制，第二部分是通过 Canvas 实现（和百度文库学的损招）反复制。除此之外，两部分共享整体的代码混淆（javascript-obfuscator）和反调试（disable-devtool）功能。

第一部分涉及的技术包括不可见 DOM 元素注入；通过 CSS 禁止文本被选中（user-select）；通过 JS 阻止鼠标事件/键盘事件/选择事件/打印事件/右键菜单事件被传播和响应。对于本部分，有三种解决思路：保存网页后解析 HTML 文件 + 按照 CSS 过滤掉不可见的部分（暴力做法）；通过设置 contentEditable 的方式卡掉 overflow-hidden 后 OCR 识别（偷鸡做法）；写 JS 删掉上面添加的种种限制（正常做法），由于做了反调试，直接在开发者工具里面执行 JS 比较困难，一个可行的方法是直接对 index.html 做修改。

本部分在网上能找到很多插件，相当一部分被卡掉了，但也有一些能用的，包括但不限于[简悦插件](https://simpread.ksria.cn/plugins/)和 [celery](http://renwenlong.com/celery/) 等，看上去简单，实际上也一点都不难，相信拦不住大家。

第二部分涉及的技术是把文字用 fillText 画到 Canvas 上达到类似图片的效果从而反复制。对于本部分，可以通过劫持 Canvas 对象的 fillText 方法拿到文本信息，由于本题做了反调试，并且劫持了 alert/confirm/prompt 三个弹窗方法，可以通过 appendChild 把文本添加到 DOM 后 OCR 或类似第一部分绕过反复制，也可以本地起一个 HTTP Server 然后把文本通过 XHR 打过去。

参考代码（DOM）：

```js
const src = document.createElement.bind(document);
document.createElement = (name, options) => {
    if (name === 'canvas') {
        const element = src(name, options);
        element.getContext('2d').fillText = (i) => {
            const node = document.createElement('div');
            node.innerHTML = i;
            document.body.appendChild(node);
        };
        return element;
    } else {
        return src(name, options);
    }
};
```

参考代码（XHR）：

```js
const src = document.createElement.bind(document);
document.createElement = (name, options) => {
    if (name === 'canvas') {
        const element = src(name, options);
        element.getContext('2d').fillText = (i) => {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', 'http://127.0.0.1:8080/' + i, true);
            xhr.send();
        };
        return element;
    } else {
        return src(name, options);
    }
};
```

## 总结

感受来自前端狗的恶意吧！另外前端终归是客户端的东西，反复制反调试之类的奇技淫巧恶心恶心人还可以，真想彻底拦住用户还是很难实现的。
