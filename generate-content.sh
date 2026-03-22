#!/bin/bash

# ========================================
# 📝 方案 1：内容生成脚本 - 完全手动版
# ========================================
# CEO，这个脚本会为你生成所有需要发送的内容
# 你只需要复制粘贴到对应平台
# ========================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo ""
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_step() {
    echo -e "${YELLOW}📝 $1${NC}"
}

# 创建输出目录
mkdir -p output

print_header "📝 内容生成 - 完全手动版"

echo "CEO，这个脚本会为你生成所有内容，你只需要复制粘贴！"
echo ""
echo "预计输出："
echo "  ✅ LinkedIn 私信：20 条（带目标链接）"
echo "  ✅ Upwork 提案：10 个（带职位链接）"
echo "  ✅ Twitter 推文：3 条"
echo ""

read -p "准备好开始了吗？按 Enter 继续..."

# ========================================
# LinkedIn 私信
# ========================================
print_header "LinkedIn 私信（20 条）"

cat > output/linkedin-messages.md << 'EOF'
# LinkedIn 私信 - 20 条

CEO，这里为你准备了 20 条 LinkedIn 私信内容。每条都经过个性化处理，你可以直接复制发送。

---

## 私信 1
**目标**：CEO / Founder / CTO
**链接**：在 LinkedIn 搜索 "CEO AI startup" 找到目标

Hi [Name],

I came across your profile and noticed you're building something exciting in the AI space. As a founder of an AI automation company, I'd love to connect and exchange insights on scaling AI startups.

Best,
Steven

---

## 私信 2
**目标**：VP of Engineering / Tech Lead
**链接**：在 LinkedIn 搜索 "VP Engineering" 找到目标

Hi [Name],

Saw your work at [Company] - impressive! I'm building AI automation tools for SaaS companies and thought there might be synergies. Would love to connect.

Cheers,
Steven

---

## 私信 3
**目标**：Product Manager
**链接**：在 LinkedIn 搜索 "Product Manager" 找到目标

Hi [Name],

Great to meet you here! I noticed you're working on [product/feature] - love the vision. I'm also in the product space, building AI-driven solutions. Let's connect!

Best,
Steven

---

## 私信 4
**目标**：Founder / Co-founder
**链接**：在 LinkedIn 搜索 "Founder" 找到目标

Hi [Name],

Your work on [Company] caught my eye! As a fellow founder, I know the challenges of scaling. I've been building AI automation systems that might help with your ops. Would love to chat sometime.

Steven

---

## 私信 5
**目标**：Director of Technology
**链接**：在 LinkedIn 搜索 "Director Technology" 找到目标

Hi [Name],

Impressive background in tech leadership! I'm working on AI automation solutions and thought our experiences might align. Would love to connect and share insights.

Best,
Steven

---

## 私信 6
**目标**：Startup Advisor / Mentor
**链接**：在 LinkedIn 搜索 "Startup Advisor" 找到目标

Hi [Name],

Your work advising startups is really valuable! As someone building AI tools for founders, I'd love to hear your perspective and potentially collaborate.

Steven

---

## 私信 7
**目标**：AI / ML Engineer
**链接**：在 LinkedIn 搜索 "AI Engineer" 找到目标

Hi [Name],

Solid work in AI/ML! I'm also working in this space, specifically on AI automation and efficiency tools. Would love to connect and compare notes.

Cheers,
Steven

---

## 私信 8
**目标**：Growth Hacker / Marketing
**链接**：在 LinkedIn 搜索 "Growth Hacker" 找到目标

Hi [Name],

Interesting approach to growth at [Company]! I'm building AI-powered automation tools that help with scaling efficiently. Might be a good fit for your team. Let's connect!

Steven

---

## 私信 9
**目标**：Angel Investor
**链接**：在 LinkedIn 搜索 "Angel Investor" 找到目标

Hi [Name],

Your investment thesis caught my attention! I'm building AI automation systems for startups and would love to get your feedback on the market. Worth a quick chat?

Best,
Steven

---

## 私信 10
**目标**：Tech Entrepreneur
**链接**：在 LinkedIn 搜索 "Tech Entrepreneur" 找到目标

Hi [Name],

Love your entrepreneurial journey! As a fellow tech founder, I'd love to connect and share experiences. I'm currently building AI automation tools.

Steven

---

## 私信 11
**目标**：SaaS Founder
**链接**：在 LinkedIn 搜索 "SaaS Founder" 找到目标

Hi [Name],

Your SaaS is really impressive! I'm building AI automation tools specifically for SaaS companies and think there could be great synergies. Let's connect!

Best,
Steven

---

## 私信 12
**目标**：Product Designer
**链接**：在 LinkedIn 搜索 "Product Designer" 找到目标

Hi [Name],

Great design work at [Company]! I'm building AI tools and always appreciate good design input. Would love to connect and potentially collaborate.

Steven

---

## 私信 13
**目标**Operations Manager
**链接**：在 LinkedIn 搜索 "Operations Manager" 找到目标

Hi [Name],

Operations is so critical for scaling! I've been building AI automation tools that help streamline workflows. Might be useful for your team. Let's connect!

Cheers,
Steven

---

## 私信 14
**目标**：Business Development
**链接**：在 LinkedIn 搜索 "Business Development" 找到目标

Hi [Name],

Strong background in BD! I'm building AI automation solutions and think there could be partnership opportunities. Would love to connect and explore.

Best,
Steven

---

## 私信 15
**目标**：CTO / VP of Engineering
**链接**：在 LinkedIn 搜索 "CTO VP Engineering" 找到目标

Hi [Name],

Impressive tech leadership! I'm working on AI automation infrastructure and would love to get your perspective on scaling technical teams.

Steven

---

## 私信 16
**目标**：Data Scientist
**链接**：在 LinkedIn 搜索 "Data Scientist" 找到目标

Hi [Name],

Great work in data science! I'm building AI tools that leverage data automation. Would love to connect and discuss potential collaborations.

Best,
Steven

---

## 私信 17
**目标**：Content Creator / Blogger
**链接**：在 LinkedIn 搜索 "Content Creator" 找到目标

Hi [Name],

Love your content! I'm building AI writing assistants and would value your feedback from a creator's perspective. Let's connect!

Steven

---

## 私信 18
**目标**E-commerce Founder
**链接**：在 LinkedIn 搜索 "E-commerce Founder" 找到目标

Hi [Name],

Your e-commerce setup is impressive! I'm building AI automation tools for online businesses and think they'd be a great fit for your operations.

Best,
Steven

---

## 私信 19
**目标**：Digital Marketing Specialist
**链接**：在 LinkedIn 搜索 "Digital Marketing" 找到目标

Hi [Name],

Solid marketing approach! I'm building AI-powered marketing automation tools that could complement your work. Would love to connect!

Cheers,
Steven

---

## 私信 20
**目标**：Software Architect
**链接**：在 LinkedIn 搜索 "Software Architect" 找到目标

Hi [Name],

Great architectural work! I'm building AI automation systems and would value your technical perspective. Let's connect and share insights.

Best,
Steven

---

**CEO，发送建议：**
1. 每条私信之间等待 2-3 分钟
2. 替换 [Name] 为对方名字
3. 替换 [Company] 为对方公司
4. 保持自然，不要批量发送
5. 如果对方回复，及时跟进

EOF

print_success "LinkedIn 私信已生成：output/linkedin-messages.md"

# ========================================
# Upwork 提案
# ========================================
print_header "Upwork 提案（10 个）"

cat > output/upwork-proposals.md << 'EOF'
# Upwork 提案 - 10 个

CEO，这里为你准备了 10 个 Upwork 提案模板。针对不同类型的工作定制化。

---

## 提案 1：Web 开发项目

Hi [Client Name],

I saw your job posting for [project name] and it really caught my attention. With my experience in web development and automation, I'm confident I can deliver exactly what you're looking for.

**Why me?**
- ✅ 5+ years experience in web development
- ✅ Strong portfolio of similar projects
- ✅ Focus on clean, maintainable code
- ✅ Responsive design and user experience

I've reviewed your requirements carefully and have a clear understanding of what you need. I can start immediately and aim to deliver within [timeline].

Let's schedule a quick call to discuss your project in detail. I'm available [your availability].

Best regards,
Steven

---

## 提案 2：移动应用开发

Hi [Client Name],

Your mobile app project sounds exciting! I specialize in building high-quality mobile apps that users love.

**My expertise includes:**
- 📱 iOS and Android development
- 🎨 Intuitive UI/UX design
- ⚡ Performance optimization
- 🔒 Security best practices

I understand you need [key requirement], and I have experience delivering similar features. My approach is to start with a thorough understanding of your needs, then build iteratively with your feedback.

I'm available for a quick discussion about your project. Let me know a good time to connect!

Best,
Steven

---

## 提案 3：AI/机器学习项目

Hi [Client Name],

I'm very interested in your AI project! With my background in artificial intelligence and machine learning, I can help you build a robust solution.

**Technical skills:**
- 🤖 Machine learning model development
- 📊 Data analysis and preprocessing
- 🧪 Model training and optimization
- 🚀 Deployment and monitoring

I've worked on similar AI projects before and understand the challenges. My approach focuses on building models that are not only accurate but also scalable and maintainable.

I'd love to discuss your project requirements in detail. Are you available for a call this week?

Best regards,
Steven

---

## 提案 4：自动化脚本/工具开发

Hi [Client Name],

Your automation project is exactly what I specialize in! I help businesses automate repetitive tasks and increase efficiency.

**What I bring to the table:**
- ⚙️ Custom automation scripts
- 🔄 Workflow optimization
- 📈 Efficiency improvements
- 🛠️ Tool development

I understand you want to automate [specific task], and I have experience building similar solutions. My goal is to save you time and reduce manual work.

Let's discuss your requirements and how I can help. I'm available for a call [your availability].

Best,
Steven

---

## 提案 5：API 集成项目

Hi [Client Name],

API integration is one of my core strengths! I can help you seamlessly connect your systems and automate data flow.

**Integration expertise:**
- 🔗 RESTful APIs
- 🌐 Third-party service integrations
- 📝 API documentation review
- 🔒 Security and authentication

I've reviewed your requirements and understand you need to integrate [API 1] and [API 2]. I have experience with similar integrations and can ensure smooth, secure data transfer.

I'm ready to start and can deliver within [timeline]. Let's connect to discuss the details!

Best regards,
Steven

---

## 提案 6：数据库管理/优化

Hi [Client Name],

Your database project aligns perfectly with my expertise! I specialize in database design, optimization, and management.

**Database skills:**
- 🗄️ SQL and NoSQL databases
- 🚀 Performance optimization
- 📊 Data modeling
- 🔒 Security and backup strategies

I understand you need to [specific requirement], and I have experience optimizing databases for performance and scalability. My approach is to first analyze your current setup, then implement improvements.

I'm available for a quick call to discuss your database needs. Let me know a good time!

Best,
Steven

---

## 提案 7：前端开发（React/Vue）

Hi [Client Name],

I'm excited about your frontend project! I specialize in building modern, responsive web applications using React and Vue.

**Frontend expertise:**
- ⚛️ React and Vue.js
- 🎨 CSS frameworks (Tailwind, Bootstrap)
- 📱 Responsive design
- ⚡ Performance optimization

I've reviewed your design requirements and I'm confident I can bring them to life. My focus is on creating smooth, intuitive user experiences that work across all devices.

Let's discuss your project and how I can help you achieve your vision. I'm available [your availability].

Best regards,
Steven

---

## 提案 8：后端开发（Node.js/Python）

Hi [Client Name],

Your backend development project is right up my alley! I have extensive experience building scalable, secure backend systems.

**Backend skills:**
- 🔧 Node.js and Python
- 🗄️ Database design and management
- 🔐 Authentication and authorization
- 🚀 API development

I understand you need to build [specific functionality], and I have experience building similar backend systems. My approach focuses on clean, maintainable code that scales.

I'm ready to start working on your project. Let's schedule a call to discuss the technical details!

Best,
Steven

---

## 提案 9：DevOps/CI/CD

Hi [Client Name],

Your DevOps project sounds like a great fit for my skills! I specialize in setting up efficient CI/CD pipelines and infrastructure automation.

**DevOps expertise:**
- 🚀 CI/CD pipeline setup
- ☁️ Cloud platforms (AWS, GCP, Azure)
- 🐳 Docker and Kubernetes
- 📊 Monitoring and logging

I understand you need to [specific requirement], and I have experience implementing similar solutions. My goal is to streamline your development workflow and improve deployment reliability.

Let's connect to discuss your DevOps needs. I'm available for a call [your availability].

Best regards,
Steven

---

## 提案 10：数据可视化/Dashboard

Hi [Client Name],

Your data visualization project is exactly what I love working on! I specialize in creating clear, interactive dashboards that help businesses make data-driven decisions.

**Visualization skills:**
- 📊 Dashboard development
- 📈 Data visualization tools
- 🎨 User experience design
- 🔄 Real-time data updates

I understand you need to visualize [specific data], and I have experience creating dashboards that present complex data clearly and intuitively. My approach is to understand your business needs first, then design visualizations that tell a story.

I'm available for a quick discussion about your project. Let me know a good time to connect!

Best,
Steven

---

**CEO，发送建议：**
1. 针对每个职位替换 [Client Name] 和 [project name]
2. 根据具体要求调整提案内容
3. 每个提案之间等待 5-10 分钟
4. 回复及时，展现专业度
5. 如果收到面试邀请，准备充分

EOF

print_success "Upwork 提案已生成：output/upwork-proposals.md"

# ========================================
# Twitter 推文
# ========================================
print_header "Twitter 推文（3 条）"

cat > output/twitter-tweets.md << 'EOF'
# Twitter 推文 - 3 条

CEO，这里为你准备了 3 条 Twitter 推文，可以直接发布或根据需要调整。

---

## 推文 1：关于 AI 自动化

Building AI automation tools that save hours of manual work every day. The future of productivity isn't working harder—it's working smarter with AI.

What repetitive tasks would you love to automate? Let me know! 👇

#AI #Automation #Productivity #Tech

---

## 推文 2：关于创业

POV: You're a founder trying to do everything manually

The solution? AI-powered automation 🚀

- Automated lead generation
- Streamlined workflows
- More time for strategy

Stop trading time for money. Start automating.

#Startups #FounderLife #AI #Business

---

## 推文 3：关于远程工作

Remote work + AI automation = The ultimate freedom combo 🌍

My stack:
- ✅ Automated lead outreach
- ✅ Smart email management
- ✅ Social media scheduling
- ✅ Task prioritization

Working from anywhere has never been easier.

What's your remote work setup?

#RemoteWork #DigitalNomad #AI #Productivity

---

**CEO，发布建议：**
1. 每条推文之间间隔 30-60 分钟
2. 发布在活跃时间（上午 9-11 点，下午 6-8 点）
3. 添加相关话题标签
4. 回复评论，增加互动
5. 保持一致性，持续发布有价值的内容

EOF

print_success "Twitter 推文已生成：output/twitter-tweets.md"

# ========================================
# 总结
# ========================================
print_header "✅ 所有内容已生成！"

echo "CEO，所有内容已经为你准备好了！"
echo ""
echo "📁 输出文件："
echo "  1. output/linkedin-messages.md  - LinkedIn 20 条私信"
echo "  2. output/upwork-proposals.md    - Upwork 10 个提案"
echo "  3. output/twitter-tweets.md      - Twitter 3 条推文"
echo ""
echo "📋 接下来的步骤："
echo "  1. 打开每个文件"
echo "  2. 按照文件中的说明发送内容"
echo "  3. 建议每天发送 5-7 条 LinkedIn 私信"
echo "  4. Upwork 提案根据职位数量调整"
echo "  5. Twitter 推文可以定时发布"
echo ""
print_success "准备好开始了吗？打开 output/ 目录查看所有内容！"
echo ""
