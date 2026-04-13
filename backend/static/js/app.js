const state = {
    topics: [],
    selectedTopic: null,
    selectedTab: "text",
    conceptMap: {},
};

const tabLabels = {
    text: "Text",
    audio: "Audio",
    image: "Image",
    video: "Video",
    youtube: "YouTube",
};

const elements = {
    topicsList: document.getElementById("topics-list"),
    topicTitle: document.getElementById("topic-title"),
    topicMeta: document.getElementById("topic-meta"),
    topicDescription: document.getElementById("topic-description"),
    resourceArea: document.getElementById("resource-area"),
    sectionsList: document.getElementById("sections-list"),
    tabBar: document.getElementById("tab-bar"),
    searchForm: document.getElementById("search-form"),
    searchInput: document.getElementById("topic-search"),
    reloadTopics: document.getElementById("reload-topics"),
    modal: document.getElementById("concept-modal"),
    modalBody: document.getElementById("modal-body"),
    modalClose: document.getElementById("modal-close"),
    topicCount: document.getElementById("topic-count"),
    activeTabLabel: document.getElementById("active-tab-label"),
};

async function fetchJSON(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
    }
    return response.json();
}

function extractListPayload(payload) {
    if (Array.isArray(payload)) {
        return payload;
    }
    if (payload && Array.isArray(payload.results)) {
        return payload.results;
    }
    return [];
}

function escapeHtml(value = "") {
    return value
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function youtubeEmbedUrl(url) {
    try {
        const parsed = new URL(url);
        if (parsed.hostname.includes("youtu.be")) {
            return `https://www.youtube.com/embed/${parsed.pathname.slice(1)}`;
        }
        const videoId = parsed.searchParams.get("v");
        if (videoId) {
            return `https://www.youtube.com/embed/${videoId}`;
        }
    } catch (error) {
        console.error(error);
    }
    return url;
}

function renderTopics() {
    elements.topicCount.textContent = String(state.topics.length);

    if (!state.topics.length) {
        elements.topicsList.innerHTML = `
            <div class="empty-note">
                No topics found. Add a topic from Django admin, then reload this page.
            </div>
        `;
        return;
    }

    elements.topicsList.innerHTML = state.topics
        .map((topic) => {
            const activeClass = state.selectedTopic?.id === topic.id ? "active" : "";
            return `
                <button class="topic-button ${activeClass}" type="button" data-topic-id="${topic.id}">
                    <h3>${escapeHtml(topic.title)}</h3>
                    <p>${escapeHtml(topic.short_description || "No short description yet.")}</p>
                </button>
            `;
        })
        .join("");
}

function filterResources(resourceType) {
    if (!state.selectedTopic) return [];
    return (state.selectedTopic.resources || []).filter(
        (resource) => resource.resource_type === resourceType
    );
}

function renderTextWithConceptLinks(text, conceptLinks) {
    if (!text) {
        return `<div class="status-message">This text resource is empty.</div>`;
    }

    const sorted = [...(conceptLinks || [])].sort((a, b) => a.start_offset - b.start_offset);
    let currentIndex = 0;
    let result = "";
    const appendEscapedText = (segment) => {
        result += escapeHtml(segment).replaceAll("\n", "<br>");
    };

    sorted.forEach((concept) => {
        const start = Number(concept.start_offset);
        const end = Number(concept.end_offset);

        if (Number.isNaN(start) || Number.isNaN(end) || start < currentIndex || end > text.length) {
            return;
        }

        appendEscapedText(text.slice(currentIndex, start));
        result += `<button type="button" class="concept-link" data-concept-id="${concept.id}">${escapeHtml(text.slice(start, end))}</button>`;
        currentIndex = end;
    });

    appendEscapedText(text.slice(currentIndex));
    return result;
}

function renderResourceCard(resource) {
    const chips = [
        `<span class="resource-chip">${tabLabels[resource.resource_type] || resource.resource_type}</span>`,
        resource.is_featured ? `<span class="resource-chip">Featured</span>` : "",
    ].join("");

    if (resource.resource_type === "text") {
        return `
            <article class="resource-card">
                <h3>${escapeHtml(resource.title)}</h3>
                <div class="resource-meta">${chips}</div>
                <div class="resource-text">
                    ${renderTextWithConceptLinks(resource.text_content || "", resource.concept_links)}
                </div>
            </article>
        `;
    }

    if (resource.resource_type === "audio") {
        return `
            <article class="resource-card">
                <h3>${escapeHtml(resource.title)}</h3>
                <div class="resource-meta">${chips}</div>
                <audio class="audio-player" controls src="${escapeHtml(resource.file_url || "")}"></audio>
            </article>
        `;
    }

    if (resource.resource_type === "image") {
        return `
            <article class="resource-card">
                <h3>${escapeHtml(resource.title)}</h3>
                <div class="resource-meta">${chips}</div>
                <div class="media-frame">
                    <img src="${escapeHtml(resource.file_url || "")}" alt="${escapeHtml(resource.title)}">
                </div>
            </article>
        `;
    }

    if (resource.resource_type === "video") {
        return `
            <article class="resource-card">
                <h3>${escapeHtml(resource.title)}</h3>
                <div class="resource-meta">${chips}</div>
                <div class="media-frame">
                    <video controls src="${escapeHtml(resource.file_url || "")}"></video>
                </div>
            </article>
        `;
    }

    if (resource.resource_type === "youtube") {
        return `
            <article class="resource-card">
                <h3>${escapeHtml(resource.title)}</h3>
                <div class="resource-meta">${chips}</div>
                <div class="youtube-frame">
                    <iframe
                        src="${escapeHtml(youtubeEmbedUrl(resource.youtube_url || ""))}"
                        title="${escapeHtml(resource.title)}"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowfullscreen
                    ></iframe>
                </div>
            </article>
        `;
    }

    return `
        <article class="resource-card">
            <h3>${escapeHtml(resource.title)}</h3>
            <div class="status-message">Unsupported resource type.</div>
        </article>
    `;
}

function renderResources() {
    if (!state.selectedTopic) {
        elements.resourceArea.innerHTML = `
            <div class="empty-state">
                <h3>No topic selected yet</h3>
                <p>Pick a topic from the left to load its resources.</p>
            </div>
        `;
        return;
    }

    const resources = filterResources(state.selectedTab);
    if (!resources.length) {
        elements.resourceArea.innerHTML = `
            <div class="empty-state">
                <h3>No ${tabLabels[state.selectedTab]} resource yet</h3>
                <p>Add a ${tabLabels[state.selectedTab].toLowerCase()} resource for this topic from Django admin.</p>
            </div>
        `;
        return;
    }

    elements.resourceArea.innerHTML = resources.map(renderResourceCard).join("");
}

function renderSections() {
    if (!state.selectedTopic || !(state.selectedTopic.sections || []).length) {
        elements.sectionsList.innerHTML = `
            <div class="empty-note">
                Introduction, detailed explanation, and additional resources will appear here.
            </div>
        `;
        return;
    }

    const sections = [...state.selectedTopic.sections].sort((a, b) => a.sort_order - b.sort_order);
    elements.sectionsList.innerHTML = sections
        .map(
            (section, index) => `
                <article class="accordion-item">
                    <button class="accordion-trigger" type="button" data-accordion-index="${index}">
                        <span>${escapeHtml(section.title)}</span>
                        <span>+</span>
                    </button>
                    <div class="accordion-content ${index === 0 ? "" : "hidden"}">
                        ${escapeHtml(section.content).replaceAll("\n", "<br>")}
                    </div>
                </article>
            `
        )
        .join("");
}

function updateTopicMeta() {
    elements.activeTabLabel.textContent = tabLabels[state.selectedTab] || state.selectedTab;

    if (!state.selectedTopic) {
        elements.topicTitle.textContent = "Choose a topic";
        elements.topicMeta.textContent = "Waiting for selection";
        elements.topicDescription.textContent =
            "Select a topic from the left panel to load text, audio, image, video, and YouTube resources.";
        return;
    }

    elements.topicTitle.textContent = state.selectedTopic.title;
    elements.topicMeta.textContent = `${state.selectedTopic.resources.length} resources · ${state.selectedTopic.sections.length} sidebar sections`;
    elements.topicDescription.textContent =
        state.selectedTopic.short_description || "This topic is ready for interactive study.";
}

async function loadTopics(query = "") {
    const search = query ? `?q=${encodeURIComponent(query)}` : "";
    elements.topicsList.innerHTML = `<div class="status-message">Loading topics...</div>`;
    const payload = await fetchJSON(`/api/topics/${search}`);
    const topics = extractListPayload(payload);
    state.topics = topics;
    if (state.selectedTopic) {
        const updated = topics.find((topic) => topic.id === state.selectedTopic.id);
        if (!updated) {
            state.selectedTopic = null;
        }
    }
    renderTopics();

    if (!state.selectedTopic && topics.length) {
        await selectTopic(topics[0].id);
    }
}

async function selectTopic(topicId) {
    elements.resourceArea.innerHTML = `<div class="status-message">Loading topic details...</div>`;
    const topic = await fetchJSON(`/api/topics/${topicId}/`);
    state.selectedTopic = topic;
    state.selectedTab = "text";
    state.conceptMap = {};
    (topic.resources || []).forEach((resource) => {
        (resource.concept_links || []).forEach((concept) => {
            state.conceptMap[String(concept.id)] = concept;
        });
    });
    renderTopics();
    updateActiveTab();
    updateTopicMeta();
    renderResources();
    renderSections();
}

function updateActiveTab() {
    elements.activeTabLabel.textContent = tabLabels[state.selectedTab] || state.selectedTab;
    elements.tabBar.querySelectorAll(".tab-button").forEach((button) => {
        button.classList.toggle("active", button.dataset.tab === state.selectedTab);
    });
}

function openModal(concept) {
    const blocks = [];

    if (concept.popup_text) {
        blocks.push(`<p>${escapeHtml(concept.popup_text).replaceAll("\n", "<br>")}</p>`);
    }
    if (concept.popup_image_url) {
        blocks.push(`
            <div class="media-frame">
                <img src="${escapeHtml(concept.popup_image_url)}" alt="${escapeHtml(concept.popup_title || concept.label)}">
            </div>
        `);
    }
    if (concept.popup_audio_url) {
        blocks.push(`<audio class="audio-player" controls src="${escapeHtml(concept.popup_audio_url)}"></audio>`);
    }
    if (concept.popup_video_url) {
        blocks.push(`
            <div class="media-frame">
                <video controls src="${escapeHtml(concept.popup_video_url)}"></video>
            </div>
        `);
    }
    if (concept.popup_youtube_url) {
        blocks.push(`
            <div class="youtube-frame">
                <iframe
                    src="${escapeHtml(youtubeEmbedUrl(concept.popup_youtube_url))}"
                    title="${escapeHtml(concept.popup_title || concept.label)}"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen
                ></iframe>
            </div>
        `);
    }

    elements.modalBody.innerHTML = `
        <h2 id="modal-title">${escapeHtml(concept.popup_title || concept.label)}</h2>
        ${blocks.join("")}
    `;
    elements.modal.classList.remove("hidden");
    elements.modal.setAttribute("aria-hidden", "false");
}

function closeModal() {
    elements.modal.classList.add("hidden");
    elements.modal.setAttribute("aria-hidden", "true");
    elements.modalBody.innerHTML = "";
}

function attachEvents() {
    elements.searchForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        await loadTopics(elements.searchInput.value.trim());
    });

    elements.reloadTopics.addEventListener("click", async () => {
        elements.searchInput.value = "";
        await loadTopics();
    });

    elements.topicsList.addEventListener("click", async (event) => {
        const topicButton = event.target.closest("[data-topic-id]");
        if (!topicButton) return;
        await selectTopic(topicButton.dataset.topicId);
    });

    elements.tabBar.addEventListener("click", (event) => {
        const tabButton = event.target.closest("[data-tab]");
        if (!tabButton) return;
        state.selectedTab = tabButton.dataset.tab;
        updateActiveTab();
        renderResources();
    });

    elements.resourceArea.addEventListener("click", (event) => {
        const conceptButton = event.target.closest(".concept-link");
        if (!conceptButton) return;
        const concept = state.conceptMap[conceptButton.dataset.conceptId];
        if (!concept) return;
        openModal(concept);
    });

    elements.sectionsList.addEventListener("click", (event) => {
        const trigger = event.target.closest(".accordion-trigger");
        if (!trigger) return;
        const content = trigger.nextElementSibling;
        const sign = trigger.querySelector("span:last-child");
        const item = trigger.closest(".accordion-item");
        content.classList.toggle("hidden");
        item.classList.toggle("open", !content.classList.contains("hidden"));
        sign.textContent = content.classList.contains("hidden") ? "+" : "−";
    });

    elements.modalClose.addEventListener("click", closeModal);
    elements.modal.addEventListener("click", (event) => {
        if (event.target.dataset.closeModal === "true") {
            closeModal();
        }
    });
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeModal();
        }
    });
}

async function init() {
    attachEvents();
    updateActiveTab();
    updateTopicMeta();
    await loadTopics();
}

init().catch((error) => {
    console.error(error);
    elements.resourceArea.innerHTML = `
        <div class="status-message">Frontend initialization failed. Check the console and backend server.</div>
    `;
});
