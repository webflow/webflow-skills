"""Trigger accuracy tests for webflow-designer-tools:page-structure skill.

Tests whether the skill activates (or doesn't) from natural language prompts.
No /page-structure prefix — relies on skill description matching.
"""
import pytest
from conftest import run_claude, extract_skill_invocations
from constants import MAX_TURNS_TRIGGER


SKILL_NAME = "webflow-designer-tools:page-structure"


# -- Positive Triggers (SHOULD activate page-structure) --

@pytest.mark.trigger
@pytest.mark.designer
class TestPageStructurePositiveTriggers:

    @pytest.fixture(autouse=True)
    def _shared(self):
        """Shared config for trigger tests."""
        self.max_turns = MAX_TURNS_TRIGGER

    def _assert_skill_triggered(self, prompt: str) -> None:
        events = run_claude(prompt=prompt, max_turns=self.max_turns)
        skills = extract_skill_invocations(events)
        assert SKILL_NAME in skills, (
            f"Expected {SKILL_NAME} to trigger for: '{prompt}'. "
            f"Skills triggered: {skills}"
        )

    def test_trigger_add_section(self):
        """'Add a hero section to my Webflow page' -> page-structure"""
        self._assert_skill_triggered("Add a hero section to my Webflow page")

    def test_trigger_build_layout(self):
        """'Build a three-column grid layout on the homepage' -> page-structure"""
        self._assert_skill_triggered("Build a three-column grid layout on the homepage")

    def test_trigger_list_elements(self):
        """'Show me all the elements on this page' -> page-structure"""
        self._assert_skill_triggered("Show me all the elements on this page")

    def test_trigger_edit_element(self):
        """'Change the heading text in the hero section' -> page-structure"""
        self._assert_skill_triggered("Change the heading text in the hero section")

    def test_trigger_components_list(self):
        """'List the components I can use on this page' -> page-structure"""
        self._assert_skill_triggered("List the components I can use on this page")

    def test_trigger_update_component(self):
        """'Update the text in my navbar component' -> page-structure"""
        self._assert_skill_triggered("Update the text in my navbar component")

    def test_trigger_create_page(self):
        """'Create a new landing page for my Webflow site' -> page-structure"""
        self._assert_skill_triggered("Create a new landing page for my Webflow site")

    def test_trigger_restructure(self):
        """'Reorganize the sections on my about page' -> page-structure"""
        self._assert_skill_triggered("Reorganize the sections on my about page")

    def test_trigger_add_element(self):
        """'Add a button below the hero image' -> page-structure"""
        self._assert_skill_triggered("Add a button below the hero image")

    def test_trigger_page_preview(self):
        """'Show me a preview of the current page structure' -> page-structure"""
        self._assert_skill_triggered("Show me a preview of the current page structure")

    def test_trigger_component_structure(self):
        """'What's inside my footer component?' -> page-structure"""
        self._assert_skill_triggered("What's inside my footer component?")

    def test_trigger_nested_elements(self):
        """'Create a card with an image, title, and description' -> page-structure"""
        self._assert_skill_triggered("Create a card with an image, title, and description")

    def test_trigger_delete_section(self):
        """'Remove the testimonials section from the page' -> page-structure"""
        self._assert_skill_triggered("Remove the testimonials section from the page")

    def test_trigger_style_elements(self):
        """'Make the hero section full-width with dark background' -> page-structure"""
        self._assert_skill_triggered("Make the hero section full-width with dark background")


# -- Negative Triggers (SHOULD NOT activate page-structure) --

@pytest.mark.trigger
@pytest.mark.negative
class TestPageStructureNegativeTriggers:

    @pytest.fixture(autouse=True)
    def _shared(self):
        self.max_turns = MAX_TURNS_TRIGGER

    def _assert_skill_not_triggered(self, prompt: str, expected_skill: str | None = None) -> None:
        events = run_claude(prompt=prompt, max_turns=self.max_turns)
        skills = extract_skill_invocations(events)
        assert SKILL_NAME not in skills, (
            f"Expected {SKILL_NAME} NOT to trigger for: '{prompt}'. "
            f"Skills triggered: {skills}"
        )
        if expected_skill:
            assert expected_skill in skills, (
                f"Expected '{expected_skill}' to trigger instead for: '{prompt}'. "
                f"Skills triggered: {skills}"
            )

    def test_no_trigger_cms_create(self):
        """CMS collection creation -> cms-collection-setup, NOT page-structure"""
        self._assert_skill_not_triggered(
            "Create a new blog post collection in Webflow",
            expected_skill="webflow-skills:cms-collection-setup",
        )

    def test_no_trigger_cms_update(self):
        """Bulk CMS update -> bulk-cms-update, NOT page-structure"""
        self._assert_skill_not_triggered(
            "Add 20 new blog posts to my CMS",
            expected_skill="webflow-skills:bulk-cms-update",
        )

    def test_no_trigger_publish(self):
        """Publishing -> safe-publish, NOT page-structure"""
        self._assert_skill_not_triggered(
            "Publish my Webflow site",
            expected_skill="webflow-skills:safe-publish",
        )

    def test_no_trigger_site_audit(self):
        """Site audit -> site-audit, NOT page-structure"""
        self._assert_skill_not_triggered(
            "Run a full audit of my Webflow site",
            expected_skill="webflow-skills:site-audit",
        )

    def test_no_trigger_accessibility(self):
        """Accessibility -> accessibility-audit, NOT page-structure"""
        self._assert_skill_not_triggered(
            "Check my site for WCAG accessibility issues",
            expected_skill="webflow-skills:accessibility-audit",
        )

    def test_no_trigger_asset_audit(self):
        """Asset audit -> asset-audit, NOT page-structure"""
        self._assert_skill_not_triggered(
            "Check all images for missing alt text",
            expected_skill="webflow-skills:asset-audit",
        )

    def test_no_trigger_link_check(self):
        """Link checking -> link-checker, NOT page-structure"""
        self._assert_skill_not_triggered(
            "Find broken links on my site",
            expected_skill="webflow-skills:link-checker",
        )

    def test_no_trigger_custom_code(self):
        """Custom code -> custom-code-management, NOT page-structure"""
        self._assert_skill_not_triggered(
            "Add Google Analytics tracking to my site",
            expected_skill="webflow-skills:custom-code-management",
        )

    def test_no_trigger_naming(self):
        """CSS naming -> flowkit-naming, NOT page-structure"""
        self._assert_skill_not_triggered(
            "Audit my CSS class names for FlowKit compliance",
            expected_skill="webflow-skills:flowkit-naming",
        )

    def test_no_trigger_cms_practices(self):
        """CMS advice -> cms-best-practices, NOT page-structure"""
        self._assert_skill_not_triggered(
            "How should I structure my CMS for an e-commerce site?",
            expected_skill="webflow-skills:cms-best-practices",
        )

    def test_no_trigger_code_component(self):
        """React component -> component-scaffold, NOT page-structure"""
        self._assert_skill_not_triggered(
            "Create a React code component for a carousel",
            expected_skill="webflow-code-component-skills:component-scaffold",
        )

    def test_no_trigger_cli(self):
        """CLI deploy -> webflow-cli:cloud, NOT page-structure"""
        self._assert_skill_not_triggered(
            "Deploy my site using the Webflow CLI",
            expected_skill="webflow-cli-skills:webflow-cloud-command",
        )

    def test_no_trigger_generic(self):
        """Non-Webflow question -> no skill at all"""
        events = run_claude(
            prompt="What's the weather today?",
            max_turns=self.max_turns,
        )
        skills = extract_skill_invocations(events)
        assert SKILL_NAME not in skills

    def test_no_trigger_seo(self):
        """SEO optimization -> site-audit or cms-best-practices, NOT page-structure"""
        events = run_claude(
            prompt="Optimize my page titles and meta descriptions",
            max_turns=self.max_turns,
        )
        skills = extract_skill_invocations(events)
        assert SKILL_NAME not in skills, (
            f"Expected page-structure NOT to trigger for SEO task. Skills: {skills}"
        )

    def test_no_trigger_design_variables(self):
        """Design tokens -> flowkit-naming, NOT page-structure"""
        self._assert_skill_not_triggered(
            "Set up my color palette and spacing tokens",
            expected_skill="webflow-skills:flowkit-naming",
        )
